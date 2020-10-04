import pandas as pd
import numpy as np
import os
if __name__ == "__main__":
    import sys
    sys.path.append("/Users/sumnap/github/nyg_ml_jqonline")
from back_test.employee.stocktrader import StockTrader
from back_test.employee.bookkeeper import BookKeeper
from back_test.employee.indextrader import IndexTrader
from back_test.employee.inspector import Inspector


class BaseBT(object):
    def __init__(self,capital,base_index,weight_mode,fee_rate,slide_point,start_date,end_date,trade_mode):
        self.capital = capital
        self.weight_mode = weight_mode
        self.bookkeeper = BookKeeper(ori_capital=capital,start_date = start_date)
        self.stocktrader = StockTrader(fee_rate,slide_point,self.bookkeeper,trade_mode)
        self.indextrader = IndexTrader(base_index,start_date = start_date,bookkeeper = self.bookkeeper)
        


    def run(self,datetime,stock_pool,stock_rank,total_position):
        self.bookkeeper.newDayBegin(datetime)
        #self,Inspector.tradeableCheck(datetime,stock_pool)
        self.stocktrader.run(datetime,stock_pool,stock_rank,total_position)
        self.indextrader.run(datetime)
        self.bookkeeper.dayEnd(datetime)



if __name__ == "__main__":
    from back_test.date_interface.jq_data import login
    import jqdatasdk as jq
    from back_test.date_interface.data_api import UserDataApi
    login()
    capital = 1000000
    base_index = '000001.XSHG'
    weight_mode = ""
    fee_rate = 0.00005
    slide_point = 0.01
    start_date = "2020-07-03"
    end_date = "2020-07-13"
    trade_mode = "mean"
    total_position = 0.95
    bt = BaseBT(capital,base_index,weight_mode,fee_rate,slide_point,start_date,end_date,trade_mode)
    #stock_list = ['300031.XSHE', '002605.XSHE', '002467.XSHE', '000835.XSHE', '300052.XSHE', '300242.XSHE', '300226.XSHE', '002447.XSHE', '300295.XSHE', '600804.XSHG', '000503.XSHE', '300113.XSHE', '300043.XSHE', '300104.XSHE', '002095.XSHE']
    stock_list = ['300750.XSHE']
    from datetime import datetime, date
    from datetime import timedelta
    date_list = [date.strftime("%Y-%m-%d") for date in jq.get_trade_days(start_date=start_date, end_date=end_date, count=None)]
    print (date_list)
    for date in date_list:
        v = UserDataApi.validIndex(date,stock_list)
        stock_list_temp = np.array(stock_list)[v]
        rank = np.ones_like(stock_list_temp)

        bt.run(date,list(stock_list_temp),list(rank),total_position)
        print (bt.bookkeeper.capital)

    # stock_list = ['600367.XSHG','600360.XSHG','600361.XSHG']

    # bt.run(end_date,stock_list,rank,total_position)
    # for k,v in bt.bookkeeper.account.items():
    #     print (v['capital'])
    #     print (v['hold_state'])
    #print (bt.bookkeeper.account)
