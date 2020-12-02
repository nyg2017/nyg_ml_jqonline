

import pymongo
from back_test.data_interface.jq_data import login
import numpy as np
import jqdatasdk as jq


from back_test.data_interface.jq_mdb.table.price_table import PriceTable
from back_test.data_interface.jq_mdb.table.index_table import IndexTable





def paddingNoCode(stock_code_list,re_dict,padding = np.nan):
    res = np.full(len(stock_code_list), np.nan, dtype=np.float)
    for i,k in enumerate(stock_code_list):
        if k in re_dict.keys():
            res[i] = re_dict[k]
    return res


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
        res = paddingNoCode(stock_code_list,code_cps_dict)
        return res



    def getIndexValue(self,date_time,index):
        result = IndexTable.fetch_one_day_index(database = self.database, date = date_time,stock_list = index,fields = ['close'])
        #result = jq.get_price(index, start_date=date_time, end_date=date_time, frequency='daily', fields=['close'], skip_paused=False, fq='pre', count=None, panel=True, fill_paused=True)
        return result['close'].values


    def getSuspensionInfor(self,date_time,stock_list):
        # suspened_info_df = jq.get_price(list(stock_list), 
        #                 start_date=date_time, 
        #                 end_date=date_time, 
        #                 frequency='daily', 
        #                 fields='paused')#['paused'].T
        suspened_info_df = PriceTable.fetch_one_day_price(database = self.database, date = date_time,stock_list = stock_list,fields = ['paused'])
        code = suspened_info_df['code']
        var = suspened_info_df['paused']

        sus_dict = dict(zip(code,var))
        res = paddingNoCode(stock_list,sus_dict)
        #return np.array([sus_dict[k] == 0 for k in stock_list])
        return res == 0.0




    def getLimitInfor(self,date_time,stock_list):
        #result = jq.get_price(list(stock_list), start_date=date_time, end_date=date_time, frequency='daily', fields=['high','low'], skip_paused=False, fq='pre', count=None, panel=True, fill_paused=True)

        result = PriceTable.fetch_one_day_price(database = self.database, date = date_time,stock_list = stock_list,fields = ['high','low'])
        var = list(result['high'] - result['low'])
        code = list(result['code'])
        code_limit_dict = dict(zip(code,var))
        res = paddingNoCode(stock_list,code_limit_dict)
        #return np.array([code_limit_dict[k] != 0 for k in stock_list])
        return res != 0.0

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