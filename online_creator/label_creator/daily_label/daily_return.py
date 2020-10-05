from online_creator.label_creator.daily_label.daily_base_label import DailyLabelBase
import jqdatasdk as jq
import pandas as pd
import numpy as np


reorder = False
fields = ['open', 'close', 'low', 'high','factor', 'avg', 'pre_close', 'paused']
def return_n_day(date,params_list,stock_list,date_index_dict,inverse_date_index_dict,price_buffer):
    date_index = date_index_dict[date]    
    base_date = inverse_date_index_dict[date_index]    
    base_price = query_and_buffer(base_date,stock_list,price_buffer)
    base_price = base_price.values[:,3]
    
    re_return_f = []
    for var in params_list:
        future_date = inverse_date_index_dict[date_index + var]
        future_price = query_and_buffer(future_date,stock_list,price_buffer)
        
        if reorder:
            pass
        else:
            future_price = future_price.values[:,3]
            return_f = ((future_price - base_price)/base_price)[...,np.newaxis]
        
        #print ("return_f shape:",return_f.shape)
        re_return_f.append(return_f)
    return re_return_f


def query_and_buffer(date,stock_list,price_buffer):
    
    
    if date not in price_buffer.keys():
        p = jq.get_price(stock_list, start_date=date, end_date=date, frequency='daily', fields=fields, skip_paused=False, fq='pre', count=None, panel=False, fill_paused=True)
        price_buffer[date] = p

    return price_buffer[date]

class DailyReturn(DailyLabelBase):
    def __init__(self,cfg):
        self.params_list = cfg


    def getLabelByDate(self,date,stock_list,date_index_dict,inverse_date_index_dict):
        
        labels  = []
        price_buffer = dict()
        #print (self.cfg)
        labels = return_n_day(date,self.params_list,stock_list,date_index_dict,inverse_date_index_dict,price_buffer)

        return labels
    
    def pReturn(self,date,stock_list,date_index_dict):
        pass
    
    def groupOp(self,feature,didx):
        pass

    def check(self,didx,inst_idx):
        pass      