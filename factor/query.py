import pymongo  
import jqdatasdk as jq
import pandas as pd
import json
from data_interface.jq_mdb.util.fromat import QA_util_date_stamp
from factor.func_dic import func_dic
from data_interface.jq_data import login

class PriceTable(BaseTable):
    def __init__(self,):
        self.client = pymongo.MongoClient(host='localhost', port=27017) 
        self.factor_database = self.client["nyg_factor"]

    def queryPerDayFactor(self,table_name,date,stock_list,fields = None):
        table = self.factor_database[table_name]

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

    def queryMulDayFactor(self,table_name,start_date,end_date,stock_list):
        cursor = self.factor_database[table_name].find(
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
