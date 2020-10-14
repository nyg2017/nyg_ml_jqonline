
import os,copy
import numpy as np
import jqdatasdk as jq
import pandas as pd
from online_creator.feature_creator.daily_feature.daily_base_feature import DailyFeatureBase
from date_interface.data_api import UserDataApi



query_func_dict = {
    "volumn":UserDataApi.getVolumn,
    "turnover":UserDataApi.getTurnoverRatio
}





def queryAndBuffer(date,stock_list,buffer_dict,query_func):
    
    
    if date not in buffer_dict.keys():
        v = query_func_dict[query_func](date,stock_list)
        #p = jq.get_volomn(stock_list, start_date=date, end_date=date, frequency='daily', fields='getVolumn', skip_paused=False, fq='pre', count=None, panel=False, fill_paused=True)
        buffer_dict[date] = v

    return buffer_dict[date]



def volumnVar(date,params_list,stock_list,date_index_dict,inverse_date_index_dict,volomn_buffer):

    #base_volomn = queryAndBuffer(date,stock_list,volomn_buffer)
    volomn_buffer['volumn'] = dict()
    date_index = date_index_dict[date]    
    re_var_f = []
    for var in params_list:
        
        base_date = inverse_date_index_dict[date_index - var-1]
        future_date = inverse_date_index_dict[date_index - var]
        base_volomn = queryAndBuffer(base_date,stock_list,volomn_buffer['volumn'],"volumn")
        future_volomn = queryAndBuffer(future_date,stock_list,volomn_buffer['volumn'],"volumn")

        #base_volomn = base_volomn.values[:,2:-2]
        #future_volomn = future_volomn.values[:,2:-2]

        var_f = (future_volomn - base_volomn)/(base_volomn + 1)
        
        #print ("var_f_v shape",var_f.shape)
        re_var_f.append(var_f[...,np.newaxis])  
    
    return re_var_f


def turnover(date,params_list,stock_list,date_index_dict,inverse_date_index_dict,volomn_buffer):
    volomn_buffer['turnover'] = dict()
    date_index = date_index_dict[date]    
    re_turnover_f = []
    for n in params_list:
        base_date = inverse_date_index_dict[date_index - n]
        turnover = queryAndBuffer(base_date,stock_list,volomn_buffer['turnover'],"turnover")
        re_turnover_f.append(turnover[...,np.newaxis])
    return re_turnover_f

def SumNDayturnover(date,params_list,stock_list,date_index_dict,inverse_date_index_dict,volomn_buffer):

    #base_volomn = queryAndBuffer(date,stock_list,volomn_buffer)
    volomn_buffer['turnover'] = dict()
    date_index = date_index_dict[date]    
    re_sum_n_turnover_f = []
    base_date = inverse_date_index_dict[date_index -1]
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
    def __init__(self,cfg):
        self.cfg = cfg

    def getFeatureByDate(self,date,stock_list,date_index_dict,inverse_date_index_dict):
        
        features = []
        volomn_buffer = dict()
        #print (self.cfg)
        for key,params_list in self.cfg.items():
            
            f = func_dic[key](date,params_list,stock_list,date_index_dict,inverse_date_index_dict,volomn_buffer)

            features += f
        

        #for f in features:
        #    print (f.shape)
        return features

    
    def groupOp(self,date):
        pass

    def check(self,didx,date):
        pass  