
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
        turnover = turnover_info[column_name_dic["turnover_ratio"]]
        re_turnover_f.append(turnover[...,np.newaxis])
    return np.concatenate(tuple(re_turnover_f),axis= -1)

def SumNDayturnover(date,params_list,stock_list,date_index_dict,inverse_date_index_dict,UserDataApi):

    #base_volomn = queryAndBuffer(date,stock_list,volomn_buffer)
    volomn_buffer['turnover'] = dict()
    date_index = date_index_dict[date]    
    re_sum_n_turnover_f = []   
    base_turnover = queryAndBuffer(base_date,stock_list,volomn_buffer['turnover'],"turnover")
    temp_days_count = 1
    for n in params_list:
        
        for i in range(temp_days_count,n):
            temp_date = inverse_date_index_dict[date_index - i -1]
            base_turnover = base_turnover + queryAndBuffer(temp_date,stock_list,volomn_buffer['turnover'],"turnover")
        
        temp_days_count = n
        re_sum_n_turnover_f.append(copy.deepcopy(base_turnover)[...,np.newaxis])
    
    return re_sum_n_turnover_f


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