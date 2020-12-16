from online_creator.label_creator.daily_label.daily_base_label import DailyLabelBase
import jqdatasdk as jq
import pandas as pd
import numpy as np
from data_interface.data_api import UserDataApi

reorder = False
fields = ['open', 'close', 'low', 'high','factor', 'avg', 'pre_close', 'paused']


def return_n_day(date,params_list,stock_list,date_index_dict,inverse_date_index_dict,UserDataApi):
    date_index = date_index_dict[date] 
    base_date = inverse_date_index_dict[date_index ]
    base_price_info, column_name_dic = UserDataApi.getPriceInfo(base_date,stock_list,fields = ["close"])
    base_close_p = base_price_info[:,column_name_dic["close"]]
    re_return_f = []
    for var in params_list:
        future_date = inverse_date_index_dict[date_index + var]
        future_price_info, column_name_dic = UserDataApi.getPriceInfo(date_time = future_date,stock_code_list = stock_list,fields = ["close"])
        future_close_p = future_price_info[:,column_name_dic["close"]]
        return_f = ((future_close_p - base_close_p)/base_close_p)[...,np.newaxis]
        re_return_f.append(return_f)

    return np.concatenate(tuple(re_return_f),axis= -1)


# def query_and_buffer(date,stock_list,price_buffer):
    
    
#     if date not in price_buffer.keys():
#         p = UserDataApi.getClosePrices(date,stock_list)
#         price_buffer[date] = p

#     return price_buffer[date]

func_dic = {
    "return":return_n_day
}

class DailyPrice(DailyLabelBase):
    def __init__(self,cfg,key):
        super(DailyPrice,self).__init__(cfg,key)


    def getLabelByDate(self,date,stock_list,date_index_dict,inverse_date_index_dict,UserDataApi):
        labels = dict()
        for key,params_list in self.cfg.items():
            labels[key] = func_dic[key](date,params_list,stock_list,date_index_dict,inverse_date_index_dict,UserDataApi)
        return labels,self.name
    
    
    def groupOp(self,feature,didx):
        pass

    def check(self,didx,inst_idx):
        pass      