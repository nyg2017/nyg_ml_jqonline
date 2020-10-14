
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

def var(date,params_list,stock_list,date_index_dict,inverse_date_index_dict,price_buffer):

    #base_price = query_and_buffer(date,stock_list,price_buffer)
    date_index = date_index_dict[date]    
    re_var_f = []
    for var in params_list:
        
        base_date = inverse_date_index_dict[date_index - var-1]
        future_date = inverse_date_index_dict[date_index - var]
        base_price = query_and_buffer(base_date,stock_list,price_buffer)
        future_price = query_and_buffer(future_date,stock_list,price_buffer)
        if reorder:
            pass
        else:
            base_price = base_price.values[:,2:-2]
            future_price = future_price.values[:,2:-2]
            var_f = (future_price - base_price)/base_price
        
        #print ("var_f_p shape",var_f.shape)
        re_var_f.append(var_f)  
    
    return re_var_f

def return_n_day(date,params_list,stock_list,date_index_dict,inverse_date_index_dict,price_buffer):
    date_index = date_index_dict[date]    
    future_date = inverse_date_index_dict[date_index - 1]    
    future_price = query_and_buffer(future_date,stock_list,price_buffer)
    future_price = future_price.values[:,3]
    
    re_return_f = []
    for var in params_list:
        base_date = inverse_date_index_dict[date_index - var-1]
        base_price = query_and_buffer(base_date,stock_list,price_buffer)
        
        if reorder:
            pass
        else:
            base_price = base_price.values[:,3]
            return_f = ((future_price - base_price)/base_price)[...,np.newaxis]
        
        re_return_f.append(return_f)
    return re_return_f

def high_d_close(date,value_list,stock_list,date_index_dict,inverse_date_index_dict,price_buffer):
    base_price = query_and_buffer(date,stock_list,price_buffer).values

    high_price = base_price[:,5]
    pre_close = base_price[:,-2]
    low_price = base_price[:,4]
    high_d_pre_close = ((hight_price - pre_close)/pre_close)[...,np.newaxis]
    low_d_pre_close = ((pre_close - pre_close)/pre_close)[...,np.newaxis]

    return [high_d_pre_close,low_d_pre_close]




func_dic = {
            "var":var,
            "return":return_n_day,
            "high_d_close":high_d_close
        }
class DailyPriceFeature(DailyFeatureBase):
    def __init__(self,cfg):
        self.cfg = cfg

    def getFeatureByDate(self,date,stock_list,date_index_dict,inverse_date_index_dict):
        
        features = []
        price_buffer = dict()
        #print (self.cfg)
        for key,params_list in self.cfg.items():
            f = func_dic[key](date,params_list,stock_list,date_index_dict,inverse_date_index_dict,price_buffer)
            features = features + f
        return features

    
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