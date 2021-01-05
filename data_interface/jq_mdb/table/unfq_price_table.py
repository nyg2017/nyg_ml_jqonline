import pymongo  
from data_interface.jq_mdb.table.base_table import BaseTable
import jqdatasdk as jq
import pandas as pd
import json
from data_interface.jq_mdb.util.fromat import QA_util_date_stamp
import time


fields = ['open' , 'close' , 'low' , 'high' , 'volume' , 'money',\
     'factor' , 'high_limit','low_limit', 'avg', 'pre_close', 'paused', 'open_interest']


class UnfqPriceTable(BaseTable):
    # def __init__(self,sql_con,sql_cur):
    #     self.con = sql_con
    #     self.sql_cur = sql_cur
    def insertInfo(self,start_date,end_date):
        #
        period_trade_date = jq.get_trade_days(start_date=start_date, end_date=end_date) # include start_date,end_date
        
        for date in period_trade_date:
            print ("inserting unfq_price table,date：",date)
            securities = jq.get_all_securities(types=[], date=date)
            df = jq.get_price(security = list(securities.index),start_date=date, end_date=date, frequency='daily', fields=fields, skip_paused=False, fq='none', count=None, panel=False, fill_paused=False)
            df = self.transform_2_jq_loc(df)
            self.table.insert_many(json.loads(df.T.to_json()).values())
        
        self.createIndex()

    def createIndex(self,):
        #self.table.getIndexes()
        self.table.create_index([('date_stamp',1),('code',1)],unique = True)
        print (self.table.index_information())


    @classmethod
    def fetch_one_day_price(cls,database,date,stock_list,fields = fields):
        table = database["unfq_price_table"]
        cursor = table.find(
            {
                'code': {
                    '$in': list(stock_list)
                },
                "date_stamp":
                    {
                        "$eq": QA_util_date_stamp(date),
                    }
                
            },
            {"_id": 0},
            batch_size=10000
        )
        res = pd.DataFrame([item for item in cursor])

        return res
    
    @classmethod
    def fetch_mul_day_price(cls,database,start_date,end_date,stock_list,fields):
        table = database["unfq_price_table"]
        cursor = table.find(
            {
                'code': {
                    '$in': stock_list
                },
                "date_stamp":
                    {
                        "$lte": QA_util_date_stamp(end_date),
                        "$gte": QA_util_date_stamp(start_date)
                    }
                
            },
            {"_id": 0},
            batch_size=10000
        )
        res = pd.DataFrame([item for item in cursor])
        return res




    def transform_2_jq_loc(self,df):
    #def __transform_jq_to_qa(df, code, type_):
        if df is None or len(df) == 0:
            raise ValueError("没有聚宽数据")
            
        df.reset_index()
        df["datetime"] = df.time
        #df["code"] = code
        #$df = df.set_index("datetime", drop=False)
        df["date_stamp"] = df["datetime"].apply(lambda x: QA_util_date_stamp(x))

        return df[[
            "code",
            "open",
            "close",
            "high",
            "low",
            "volume",
            "money",
            "factor",
            "high_limit",
            'low_limit', 
            'avg', 
            'pre_close',
            'paused',
            'open_interest',
            "datetime",
            "date_stamp",
        ]]