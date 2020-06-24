
import sys
if __name__ == "__main__":
    sys.path.append("/Users/sumnap/github/nyg_ml_jqonline")

import pandas as pd
import json
import jqdatasdk as jq
from util.jqdata_processor import list2Dic,dateArr2List,dataframe2Arr
from util.leading_score import *
import datetime
import numpy as np
import os
from util.jq_init import login

#from itertools import zip

trade_date_begin = '2010-01-01'



def invert_dict(d):
    return dict(zip(d.values(), d.keys()))





class SelectLeadingOnline(object):
    def __init__(self,start_date = '2015-01-07',end_date = '2015-01-20',cfg = None):
        login()
        self.cfg = cfg
        #self.stock_list = stock_list
        self.start_date = start_date
        self.end_date = end_date
        
        self.initDateIndexDict()



    
    def initDateIndexDict(self):

        self.date_arr = jq.get_trade_days(self.start_date,self.end_date)
        self.date_list = dateArr2List(self.date_arr)

        self.trade_date_arr = jq.get_trade_days(trade_date_begin,self.end_date)
        self.trade_date_list = dateArr2List(self.trade_date_arr)
        self.date_index_dict = list2Dic(self.trade_date_list)
        self.inverse_date_index_dict =  invert_dict(self.date_index_dict )

        
        #self.inverse_stock_index_dict = invert_dict(self.stock_index_dict)
        #print (self.inverse_date_index_dict)
    
    def selectLeadingFromGroup(self,stock_list,leading_percent = 0.2,weights = 0.7):
        #print (stock_list)
        stock_index_dict = list2Dic(stock_list)
        price_socre = self.getWeightPriceScore(stock_list,stock_index_dict,weights)
        
        total_num = price_socre.shape[0]
        sorted_price_score = np.argsort(price_socre)
        
        stock_pool_list = []

        start = int(total_num * (1-0.2))
        for i in range(start,total_num):
            idx = sorted_price_score[i]
            stock_pool_list.append(stock_list[idx])
        

    
    def getWeightPriceScore(self,stock_list,stock_index_dict,weights = 0.7):
        weight_leading_score = np.zeros(len(stock_index_dict))
        for date in self.date_list:
            print (date)
            new_score = getPriceLeadingScore(stock_list,stock_index_dict,self.date_index_dict,self.inverse_date_index_dict,date)
            mask = ~np.isnan(new_score)
            weight_leading_score[mask] = weight_leading_score[mask] * weights + new_score[mask] * (1-weights)
            
            #print (weight_leading_score)
        return weight_leading_score
    




if __name__ == "__main__":
    with open("/Users/sumnap/github/nyg_ml_plus/DATA/ori_data/industry_list/sw_l3.json","r") as f:
        industry_list = json.load(f)

    stock_list = industry_list["L72"]["stocks_list"]
    s_l = SelectLeadingOnline()

    print (stock_list)
    s_l.selectLeadingFromGroup(stock_list)
