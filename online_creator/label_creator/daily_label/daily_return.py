from online_creator.label_creator.daily_base_label import DailyLabelBase
import jqdatasdk as jq
import pandas as pd



def query_and_buffer(date,stock_list,price_buffer):
    
    
    if date not in price_buffer.keys():
        p = jq.get_price(stock_list, start_date=date, end_date=date, frequency='daily', fields=fields, skip_paused=False, fq='pre', count=None, panel=False, fill_paused=True)
        price_buffer[date] = p

    return price_buffer[date]

class DailyReturn(DailyLabelBase):
    def __init__(self,cfg):
        self.cfg = cfg


    def getFeatureByDate(self,date,stock_list,date_index_dict):
        
        for i in self.cfg:
            self.p_return(date,stock_list,date_index_dict)
    
    def p_return(self,date,stock_list,date_index_dict):
        pass
    
    def groupOp(self,feature,didx):
        pass

    def check(self,didx,inst_idx):
        pass      