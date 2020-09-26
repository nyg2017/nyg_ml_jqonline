import pandas as pd
import numpy as np
import os
if __name__ == "__main__":
    import sys
    sys.path.append("/Users/sumnap/github/nyg_ml_jqonline")
from back_test.employee.stocktrader import StockTrader
from back_test.employee.bookkeeper import BookKeeper
from back_test.employee.indextrader import IndexTrader
from date_interface.jq_data import login

class BaseBT(object):
    def __init__(self,capital,base_index,weight_mode,fee_rate,slide_point,start_date,end_date,trade_mode):
        self.capital = capital
        self.weight_mode = weight_mode
        self.bookkeeper = BookKeeper(ori_capital=capital,start_date = start_date)
        self.stocktrader = StockTrader(fee_rate,slide_point,self.bookkeeper,trade_mode)
        self.indextrader = IndexTrader(base_index,start_date = start_date,bookkeeper = self.bookkeeper)
        


    def run(self,datetime,stock_pool,stock_rank,total_position):
        self.bookkeeper.newDayBegin(datetime)
        self.stocktrader.run(datetime,stock_pool,stock_rank,total_position)
        self.indextrader.run(datetime)
        self.bookkeeper.dayEnd(datetime)



if __name__ == "__main__":
    login()
    capital = 1000000
    base_index = '000001.XSHG'
    weight_mode = ""
    fee_rate = 0.0005
    slide_point = 0.01
    start_date = "2015-01-05"
    end_date = "2015-01-06"
    trade_mode = "mean"
    total_position = 0.7
    bt = BaseBT(capital,base_index,weight_mode,fee_rate,slide_point,start_date,end_date,trade_mode)
    stock_list = ['600362.XSHG','600360.XSHG','600361.XSHG']
    rank = [0,1,2]
    bt.run(start_date,stock_list,rank,total_position)
    bt.run(end_date,stock_list,rank,total_position)
    for k,v in bt.bookkeeper.account.items():
        print (v['transaction_state'])
        print (v['hold_state'])
    #print (bt.bookkeeper.account)
