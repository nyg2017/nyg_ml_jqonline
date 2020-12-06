

import pymongo
#from data_interface.jq_data import login
import numpy as np
#import jqdatasdk as jq
from data_interface.jq_mdb.util.fromat import df2Array

from data_interface.jq_mdb.table.price_table import PriceTable
from data_interface.jq_mdb.table.index_table import IndexTable
from data_interface.jq_mdb.table.turnover_ratio_table import TurnOverRatioTable
from data_interface.jq_mdb.table.trade_days_table import TradeDayTable
from data_interface.jq_mdb.table.all_security_table import AllSecurityTable




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
        #self.login()

    def login(self):
        login()

    def getTradeDays(self,start_date,end_date):
        result = TradeDayTable.fetch_period_trade_days(self.database,start_date,end_date)
        return result

    def getClosePrices(self,date_time,stock_code_list):
        result = PriceTable.fetch_one_day_price(database = self.database, date = date_time,stock_list = stock_code_list,fields = ['close'])
        #result = jq.get_price(list(stock_code_list), start_date=date_time, end_date=date_time, frequency='daily', fields=['close'], skip_paused=False, fq='pre', count=None, panel=True, fill_paused=True)
        code = list(result['code'])
        cps = list(result['close'])
        code_cps_dict = dict(zip(code,cps))
        res = paddingNoCode(stock_code_list,code_cps_dict)
        return res

    def getPriceInfo(self,date_time,stock_code_list,fields = None):
        result = PriceTable.fetch_one_day_price(database = self.database, date = date_time,stock_list = stock_code_list,fields = fields)
        result,col_name_dic = df2Array(stock_code_list,result)
        return result,col_name_dic

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

    def getVolumn(self,date_time,stock_code_list):
        #result = jq.get_price(list(stock_code_list), start_date=date_time, end_date=date_time, frequency='daily', fields=['volume'], skip_paused=False, fq='pre', count=None, panel=True, fill_paused=True)
        result = PriceTable.fetch_one_day_price(database = self.database, date = date_time,stock_list = stock_code_list,fields = ['volume'])
        code = list(result['code'])
        cps = list(result['volume'])
        code_vol_dict = dict(zip(code,cps))
        res = paddingNoCode(stock_code_list,code_vol_dict)
        return res

    def getTurnoverRatio(self,date_time,stock_code_list,fields):
        result = TurnOverRatioTable.fetch_one_day_turnover_rate(database = self.database, date = date_time,stock_list = stock_code_list,fields = fields)
        result,col_name_dic = df2Array(stock_code_list,result)
        return result,col_name_dic

    def getMulDayTurnoverRatio(self,start_date,end_date,stock_list,fields):
        return TurnOverRatioTable.fetch_mul_day_turnover_rate(database = self.database, start_date = start_date, end_date = end_date, stock_list = stock_list , fields = fields)

    def isPublic(self,date_time,stock_list):
        v = np.zeros(len(stock_list),dtype = np.int)
        #result = jq.get_price(list(stock_list), start_date=date_time, end_date=date_time, frequency='daily', fields=['paused'], skip_paused=False, fq='pre', count=None, panel=True, fill_paused=True)
        #result = jq.get_all_securities(types=[], date=date_time)
        result = AllSecurityTable.fetch_all_security(database = self.database,date=date_time)
        #print (result)
        code_list = list(result.index)
        for i,stock in enumerate(stock_list):
            if stock in code_list:
                v[i] = 1
        return v.astype(np.bool)




if __name__ == "__main__":
    jq_loc = JqMdb()
    date = "2020-02-24"
    stock_list = ['300750.XSHE','300760.XSHE','300761.XSHE','slkhjf']
    a,name = jq_loc.getPriceInfo(date,stock_list)
    print (a.shape[1],len(name))