
import os,copy
import numpy as np
import jqdatasdk as jq
import pandas as pd
from online_creator.feature_creator.daily_feature.daily_base_feature import DailyFeatureBase
from data_interface.data_api import UserDataApi



query_func_dict = {
    "volumn":UserDataApi.getVolumn,
    "turnover":UserDataApi.getTurnoverRatio
}

def df2Array(stock_list,df):
    values = df[["code","turnover_ratio"]].values

    col_name = df.columns.values
    codes = values[:,0]
    values = values[:,1:]
    re_array = np.full((len(stock_list),values.shape[1]),fill_value = np.nan)

    for i,code in enumerate(codes):
        j = i
        while(code != stock_list[j]):
            j+=1
        codes[i] = j
    re_array[codes.tolist()] = values
    return re_array

def volumnVar(date,params_list,stock_list,date_index_dict,inverse_date_index_dict,UserDataApi):
    
    date_index = date_index_dict[date]    
    re_var_f = []
    for var in params_list:
        base_date = inverse_date_index_dict[date_index - var-1]
        future_date = inverse_date_index_dict[date_index - var]
        base_price_info, column_name_dic = UserDataApi.getPriceInfo(base_date,stock_list,fields = ["volume"])
        future_price_info, column_name_dic = UserDataApi.getPriceInfo(future_date,stock_list,fields = ["volume"])
        base_close_p = base_price_info[:,column_name_dic["volume"]]
        future_close_p = future_price_info[:,column_name_dic["volume"]]
        var_f = (future_close_p - base_close_p)/base_close_p
        re_var_f.append(var_f.reshape(-1,1)) 
    
    return np.concatenate(tuple(re_var_f),axis= -1)



def turnover(date,params_list,stock_list,date_index_dict,inverse_date_index_dict,UserDataApi):

    date_index = date_index_dict[date]    
    re_turnover_f = []
    for n in params_list:
        base_date = inverse_date_index_dict[date_index - n]
        turnover_info ,column_name_dic = UserDataApi.getTurnoverRatio(base_date,stock_list,fields = ["turnover_ratio"])
        turnover = turnover_info[:,column_name_dic["turnover_ratio"]]

        re_turnover_f.append(turnover[...,np.newaxis])
    return np.concatenate(tuple(re_turnover_f),axis= -1)

def SumNDayturnover(date,params_list,stock_list,date_index_dict,inverse_date_index_dict,UserDataApi):

    max_n = np.max(np.array(params_list))
    date_index = date_index_dict[date] 
    end_date = inverse_date_index_dict[date_index - 1]
    start_date = inverse_date_index_dict[date_index - max_n]

    mul_day_turnover_ratio = UserDataApi.getMulDayTurnoverRatio(start_date = start_date,end_date = end_date,stock_list = stock_list,fields = ["turnover_ratio"])
    include_date_list = [inverse_date_index_dict[date_index - i] for i in range(1,max_n + 1)]

    all_day_turnover_ratio_array = np.full((len(stock_list),max_n,1),fill_value=0.0,dtype=np.float)
    for i,date in enumerate(include_date_list):
        daily_df = mul_day_turnover_ratio[mul_day_turnover_ratio['day'] == date]
        daily_array = df2Array(stock_list,daily_df)
        all_day_turnover_ratio_array[:,i] = daily_array

    
    sum_n_turnover = np.full((len(stock_list),len(params_list),1),fill_value=0.0,dtype=np.float)
    for i,para in enumerate(params_list):
        sum_n_turnover[:,i] = np.sum(all_day_turnover_ratio_array[:,:i+1],axis= 1)
    # #base_volomn = queryAndBuffer(date,stock_list,volomn_buffer)
    # volomn_buffer['turnover'] = dict()
    # date_index = date_index_dict[date]    
    # re_sum_n_turnover_f = []   
    # base_turnover = queryAndBuffer(base_date,stock_list,volomn_buffer['turnover'],"turnover")
    # temp_days_count = 1
    # for n in params_list:
        
    #     for i in range(temp_days_count,n):
    #         temp_date = inverse_date_index_dict[date_index - i -1]
    #         base_turnover = base_turnover + queryAndBuffer(temp_date,stock_list,volomn_buffer['turnover'],"turnover")
        
    #     temp_days_count = n
    #     re_sum_n_turnover_f.append(copy.deepcopy(base_turnover)[...,np.newaxis])
        #print (sum_n_turnover[:,i])


    return sum_n_turnover.reshape((len(stock_list),len(params_list)))


func_dic = {
            "var":  volumnVar,
            "turnover": turnover,
            "sum_n_turnover":SumNDayturnover
        }

class DailyVolumeFeature(DailyFeatureBase):


    def getFeatureByDate(self,date,stock_list,date_index_dict,inverse_date_index_dict,UserDataApi):
        
        features = dict()
        #print (self.cfg)
        for key,params_list in self.cfg.items():
            features[key] = func_dic[key](date,params_list,stock_list,date_index_dict,inverse_date_index_dict,UserDataApi)
        
        return features,self.name

    
    def groupOp(self,date):
        pass

    def check(self,didx,date):
        pass  