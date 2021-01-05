import pymongo  
import jqdatasdk as jq
import pandas as pd
import json
from data_interface.jq_mdb.util.fromat import QA_util_date_stamp
from factor.func_dic import func_dic
from data_interface.jq_data import login

class FactorDBInsert(BaseTable):
    def __init__(self,):
        self.client = pymongo.MongoClient(host='localhost', port=27017) 
        self.factor_database = self.client["nyg_factor"]
        # self.jq_loc_database = self.client["jq_loc"]
        # login()
        
    def insertInfo(self,table_name,start_date,end_date):
        
        period_trade_date = jq.get_trade_days(start_date=start_date, end_date=end_date) # include start_date,end_date
        
        for date in period_trade_date:
            print ("inserting price table,date：",date)
            securities = jq.get_all_securities(types=[], date=date)
            df = func_dic[table_name](date)
            df = self.transform_2_jq_loc(df)
            self.table.insert_many(json.loads(df.T.to_json()).values())
        
        self.createIndex(table_name)

    def createIndex(self,):
        #self.table.getIndexes()
        self.factor_database[table_name].create_index([('date_stamp',1),('code',1)],unique = True)
        print (self.table.index_information())

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
            "date_stamp",
            "factor",
        ]]