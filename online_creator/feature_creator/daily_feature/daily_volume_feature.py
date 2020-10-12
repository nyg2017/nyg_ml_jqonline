
import os
import numpy as np
import jqdatasdk as jq
import pandas as pd
from online_creator.feature_creator.daily_feature.daily_base_feature import DailyFeatureBase
from back_test.date_interface.jq_data import getVolumn




def query_and_buffer(date,stock_list,volomn_buffer):
    
    
    if date not in volomn_buffer.keys():
        v = getVolumn(date,stock_list)
        #p = jq.get_volomn(stock_list, start_date=date, end_date=date, frequency='daily', fields='getVolumn', skip_paused=False, fq='pre', count=None, panel=False, fill_paused=True)
        volomn_buffer[date] = v

    return volomn_buffer[date]

def var(date,params_list,stock_list,date_index_dict,inverse_date_index_dict,volomn_buffer):

    #base_volomn = query_and_buffer(date,stock_list,volomn_buffer)
    date_index = date_index_dict[date]    
    re_var_f = []
    for var in params_list:
        
        base_date = inverse_date_index_dict[date_index - var-1]
        future_date = inverse_date_index_dict[date_index - var]
        base_volomn = query_and_buffer(base_date,stock_list,volomn_buffer)
        future_volomn = query_and_buffer(future_date,stock_list,volomn_buffer)
        if reorder:
            pass
        else:
            base_volomn = base_volomn.values[:,2:-2]
            future_volomn = future_volomn.values[:,2:-2]
            var_f = (future_volomn - base_volomn)/base_volomn
        
        #print ("var_f shape",var_f.shape)
        re_var_f.append(var_f)  
    
    return re_var_f


func_dic = {
            "var":var,
            "return":return_n_day,
            "high_d_close":high_d_close
        }

class DailyVolumeFeature(DailyFeatureBase):
    def __init__(self,cfg):
        self.cfg = cfg

    def getFeatureByDate(self,date,stock_list,date_index_dict,inverse_date_index_dict):
        
        features = []
        volomn_buffer = dict()
        #print (self.cfg)
        for key,params_list in self.cfg.items():
            f = func_dic[key](date,params_list,stock_list,date_index_dict,inverse_date_index_dict,volomn_buffer)
            features = features + f

        return features

    
    def groupOp(self,date):
        pass

    def check(self,didx,date):
        pass  