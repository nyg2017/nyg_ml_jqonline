
import os
import numpy as np
import jqdatasdk as jq
import pandas as pd
from online_creator.feature_creator.daily_feature.daily_base_feature import DailyFeatureBase
 
fields = ['open', 'close', 'low', 'high','factor', 'avg', 'pre_close', 'paused']

reorder = False


def query_and_buffer(date,stock_list,price_buffer):
      
    if date not in price_buffer.keys():
        p = jq.get_price(list(stock_list), start_date=date, end_date=date, frequency='daily', fields=fields, skip_paused=False, fq='pre', count=None, panel=False, fill_paused=True)
        price_buffer[date] = p

    return price_buffer[date]

def var(date,params_list,stock_list,date_index_dict,inverse_date_index_dict,UserDataApi):

    date_index = date_index_dict[date]    
    re_var_f = []
    for var in params_list:
        base_date = inverse_date_index_dict[date_index - var-1]
        future_date = inverse_date_index_dict[date_index - var]
        base_price_info, column_name_dic = UserDataApi.getPriceInfo(base_date,stock_list,fields = ["close"])
        future_price_info, column_name_dic = UserDataApi.getPriceInfo(future_date,stock_list,fields = ["close"])
        base_close_p = base_price_info[:,column_name_dic["close"]]
        future_close_p = future_price_info[:,column_name_dic["close"]]
        var_f = (future_close_p - base_close_p)/base_close_p
        re_var_f.append(var_f.reshape(-1,1)) 
    
    return np.concatenate(tuple(re_var_f),axis= -1)

def return_n_day(date,params_list,stock_list,date_index_dict,inverse_date_index_dict,UserDataApi):
    date_index = date_index_dict[date]    
    future_date = inverse_date_index_dict[date_index - 1]    
    future_price_info, column_name_dic = UserDataApi.getPriceInfo(future_date,stock_list,fields = ["close"])
    future_close_p = future_price_info[:,column_name_dic["close"]]

    re_return_f = []
    for var in params_list:
        base_date = inverse_date_index_dict[date_index - var-1]
        base_price_info, column_name_dic = UserDataApi.getPriceInfo(base_date,stock_list,fields = ["close"])
        base_close_p = base_price_info[:,column_name_dic["close"]]
        return_f = ((future_close_p - base_close_p)/base_close_p)[...,np.newaxis]
        re_return_f.append(return_f)
    return np.concatenate(tuple(re_return_f),axis= -1)

def high_d_close(date,params_list,stock_list,date_index_dict,inverse_date_index_dict,UserDataApi):

    date_index = date_index_dict[date]    
    re_high_d_cps_f = []
    for var in params_list:
        base_date = inverse_date_index_dict[date_index - var-1]
        future_date = inverse_date_index_dict[date_index - var]
        base_price_info, column_name_dic = UserDataApi.getPriceInfo(base_date,stock_list,fields = ["close"])
        future_price_info, column_name_dic = UserDataApi.getPriceInfo(future_date,stock_list,fields = ["high"])
        base_close_p = base_price_info[:,column_name_dic["close"]]
        future_close_p = future_price_info[:,column_name_dic["high"]]
        high_d_cps_f = (future_close_p - base_close_p)/base_close_p
        re_high_d_cps_f.append(high_d_cps_f.reshape(-1,1)) 
    
    return np.concatenate(tuple(re_high_d_cps_f),axis= -1)




func_dic = {
            "var":var,
            "return":return_n_day,
            "high_d_close":high_d_close
        }

class DailyPriceFeature(DailyFeatureBase):

    def getFeatureByDate(self,date,stock_list,date_index_dict,inverse_date_index_dict,UserDataApi):
        
        features = dict()
        for key,params_list in self.cfg.items():
            features[key] = func_dic[key](date,params_list,stock_list,date_index_dict,inverse_date_index_dict,UserDataApi)
        return features,self.name

    def groupOp(self,date):
        pass

    def check(self,didx,date):
        pass  




if __name__ == "__main__":
    cfg = {
        "var":[1,2,3,4,5]
    }


    dp_f = DailyPriceFeature(cfg)
    dp_f.getFeatureByDate()