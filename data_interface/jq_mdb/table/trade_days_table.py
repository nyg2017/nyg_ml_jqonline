import pymongo  
from data_interface.jq_mdb.table.base_table import BaseTable
import jqdatasdk as jq
import pandas as pd
import json
from data_interface.jq_mdb.util.fromat import QA_util_date_stamp,QA_util_stamp2datetime



class TradeDayTable(BaseTable):
    # def __init__(self,sql_con,sql_cur):
    #     self.con = sql_con
    #     self.sql_cur = sql_cur
    def insertInfo(self,start_date,end_date):
        #
        df = jq.get_trade_days(start_date=start_date, end_date=end_date) # include start_date,end_date
        df = pd.DataFrame(df)
        df = self.transform_2_jq_loc(df)
        self.table.insert_many(json.loads(df.T.to_json()).values())
        
        self.createIndex()

    def createIndex(self,):
        #self.table.getIndexes()
        self.table.create_index([('date_stamp',1)],unique = True)
        print (self.table.index_information())


    @classmethod
    def fetch_period_trade_days(cls,database,start_date,end_date,fields = None):
        table = database["trade_days_table"]

        cursor = table.find(
            {
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
        res = res["date_stamp"].apply(lambda x: QA_util_stamp2datetime(x).strftime("%Y-%m-%d")).values.tolist()
        return res




    def transform_2_jq_loc(self,df):
    #def __transform_jq_to_qa(df, code, type_):
        if df is None or len(df) == 0:
            raise ValueError("没有聚宽数据")
            
        df.reset_index()
        df["datetime"] = df[0]
        df["date_stamp"] = df["datetime"].apply(lambda x: QA_util_date_stamp(x))

        return df[[
            "date_stamp",
            "datetime"
        ]]