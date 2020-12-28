import pymongo  
from data_interface.jq_mdb.table.base_table import BaseTable
import jqdatasdk as jq
import pandas as pd
import json
from data_interface.jq_mdb.util.fromat import QA_util_date_stamp
from data_interface.jq_mdb.table.trade_days_table import TradeDayTable


class AllSecurityTable(BaseTable):
    # def __init__(self,sql_con,sql_cur):
    #     self.con = sql_con
    #     self.sql_cur = sql_cur
    def insertInfo(self,start_date,end_date):
        
        period_trade_date = jq.get_trade_days(start_date=start_date, end_date=end_date) # include start_date,end_date
        #period_trade_date = TradeDayTable.fetch_period_trade_days(self.database,start_date=start_date, end_date=end_date)
        for date in period_trade_date:
            print ("inserting all_security table,date：",date)
            df = jq.get_all_securities(types=[], date=date)
            df = self.transform_2_jq_loc(df,date)
            self.table.insert_many(json.loads(df.T.to_json()).values())
        self.createIndex()

    def createIndex(self,):
        #self.table.getIndexes()
        self.table.create_index([('date_stamp',1)],unique = True)
        print (self.table.index_information())


    @classmethod
    def fetch_all_security(cls,database,date,fields = None):
        table = database["all_security_table"]

        cursor = table.find(
            {
                "date_stamp":
                    {
                        "$eq": QA_util_date_stamp(date),
                    }         
            },
            {"_id": 0},
            batch_size=10000
        )
        res = pd.DataFrame([item for item in cursor])
        return res["code"].values.tolist()




    def transform_2_jq_loc(self,df,date):
    #def __transform_jq_to_qa(df, code, type_):
        if df is None or len(df) == 0:
            raise ValueError("没有聚宽数据")
            
        df.reset_index()
        df["datetime"] = date
        df["date_stamp"] = df["datetime"].apply(lambda x: QA_util_date_stamp(x))
        df["code"] = df.index

        return df[[
            "date_stamp",
            "datetime",
            "code",
            "name",
            "start_date",
            "end_date",
            "type"
        ]]