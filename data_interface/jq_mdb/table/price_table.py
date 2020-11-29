import pymongo  
from data_interface.jq_mdb.table.base_table import BaseTable
import jqdatasdk as jq
import pandas as pd
import json
fields = {'open' : 0, 'close' : 1, 'low' : 2, 'high' : 3, 'volume' : 4, 'money': 5,\
     'factor' : 6, 'high_limit' : 7,'low_limit' : 8, 'avg' : 9, 'pre_close' : 10, 'paused' : 11, 'open_interest' : 12}


class PriceTable(BaseTable):
    # def __init__(self,sql_con,sql_cur):
    #     self.con = sql_con
    #     self.sql_cur = sql_cur
    def insertInfo(self,start_date,end_date):
        #
        period_trade_date = jq.get_trade_days(start_date=start_date, end_date=end_date) # include start_date,end_date
        
        for data in period_trade_date:
            securities = jq.get_all_securities(types=[], date=data)
            df = jq.get_price(security = list(securities.index),start_date=data, end_date=data, frequency='daily', fields=fields, skip_paused=False, fq='pre', count=None, panel=False, fill_paused=False)
            self.table[data.strftime('%Y-%m-%d')].insert_many(json.loads(df.T.to_json()).values())

    def getPriceInfo(self,stock_list,date,fields = None):
        collection = self.table[date]
        df = pd.DataFrame(list(collection.find()))
        a = df.loc[df["code"].isin(stock_list)]
        print (a)
        

        