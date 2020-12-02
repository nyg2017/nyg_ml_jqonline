from back_test.data_interface.jq_mdb.table.price_table import PriceTable
import pymongo
from back_test.data_interface.jq_data import login
import numpy as np
import jqdatasdk as jq

class JqMdb(object):
    def __init__(self,):
        self.client = pymongo.MongoClient(host='localhost', port=27017) 
        self.database = self.client["jq_loc"]
        login()

    def getClosePrices(self,date_time,stock_code_list):
        result = PriceTable.fetch_one_day_price(database = self.database, date = date_time,stock_list = stock_code_list,fields = ['close'])
        #result = jq.get_price(list(stock_code_list), start_date=date_time, end_date=date_time, frequency='daily', fields=['close'], skip_paused=False, fq='pre', count=None, panel=True, fill_paused=True)
        code = list(result['code'])
        cps = list(result['close'])
        code_cps_dict = dict(zip(code,cps))
        res = []
        for k in stock_code_list:
            if k in code:
                res.append(code_cps_dict[k])
            else:
                res.append(np.nan)
        return res



    def getIndexValue(self,date_time,index):
        result = jq.get_price(index, start_date=date_time, end_date=date_time, frequency='daily', fields=['close'], skip_paused=False, fq='pre', count=None, panel=True, fill_paused=True)
        return result['close'].values


    def getSuspensionInfor(self,date_time,stock_list):
        suspened_info_df = jq.get_price(list(stock_list), 
                        start_date=date_time, 
                        end_date=date_time, 
                        frequency='daily', 
                        fields='paused')#['paused'].T
        code = suspened_info_df['code']
        var = suspened_info_df['paused']
        sus_dict = dict(zip(code,var))
        return np.array([sus_dict[k] == 0 for k in stock_list])




    def getLimitInfor(self,date_time,stock_list):
        result = jq.get_price(list(stock_list), start_date=date_time, end_date=date_time, frequency='daily', fields=['high','low'], skip_paused=False, fq='pre', count=None, panel=True, fill_paused=True)
        var = list(result['high'] - result['low'])
        code = list(result['code'])
        code_limit_dict = dict(zip(code,var))
        return np.array([code_limit_dict[k] != 0 for k in stock_list])

    def validIndex(self,date_time,stock_list):
        a = self.getSuspensionInfor(date_time,stock_list)
        b = self.getLimitInfor(date_time,stock_list)
        v = np.logical_and(a,b)
        return v


    if __name__ == "__main__":
        login()
        code = ["300313.XSHE","300315.XSHE","300316.XSHE"]
        date_time = "2020-09-11"
        
        panel = self.getVolumn(date_time,code)
        print (panel)




if __name__ == "__main__":
    jq_loc = JqMdb()