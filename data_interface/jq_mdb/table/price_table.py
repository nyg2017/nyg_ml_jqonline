import pymongo  
from data_interface.jq_mdb.table.base_table import BaseTable
import jqdatasdk as jq
import pandas as pd
import json
from data_interface.jq_mdb.util.fromat import QA_util_date_stamp

fields = ['open' , 'close' , 'low' , 'high' , 'volume' , 'money',\
     'factor' , 'high_limit','low_limit', 'avg', 'pre_close', 'paused', 'open_interest']


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
            df = self.transform_2_jq_loc(df)
            self.table.insert_many(json.loads(df.T.to_json()).values())

    def createIndex(self,):
        #self.table.getIndexes()
        self.table.create_index([('date_stamp',1),('code',1)])
        print (self.table.index_information())

    def fetch(self,date,stock_list,fields):
        cursor = self.table.find(
            {
                'code': {
                    '$in': stock_list
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