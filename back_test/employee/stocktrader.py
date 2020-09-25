import pandas as pd
import numpy as np
import os
from back_test.employee.positionspilitor import PositionSpilitor

class StockTrader(object):
    def __init__(self,fee_rate,slide_point,bookkeeper,trade_mode):
        self.fee = fee_rate
        self.slide_point = slide_point
        self.trade_mode = trade_mode
        self.bookkeeper = bookkeeper
        self.position_spilitor = PositionSpilitor(trade_mode)


    '''
    def extend_target_hold_dict(self,ori_hold_dict,target_hold_dict):
        for k in ori_hold_dict.keys():
            if k not in target_hold_dict.keys():
                target_hold_dict[k] = 
        
        return target_hold_dict
    '''

    def buyOrSell(self,target_code,target_info,last_hold_by_code):
        las_hold_num = last_hold_by_code['hold_num']
        target_hold_num = target_info['target_num']
        if target_hold_num > ori_hold_num:
            buy()
        elif target_hold_num < ori_hold_num:
            sell()
        else:
            pass
            

    def tradeByDatetime(self,last_account_dict,target_hold_dict):
        #target_hold_dict_extend = self.extend_target_hold_dict(ori_hold_dict,target_hold_dict)
        last_account_hold_dict = last_account_dict['hold_state']
        for k,v in target_hold_dict.items():
            if k not in last_account_hold_dict.keys():
                last_hold_by_code = self.bookkeeper.initCodeInfoForHoldState(aver_cost = 0, market_price = 0, hold_num = 0)
            else:
                last_hold_by_code = last_account_hold_dict[k]
            
            self.buyOrSell(target_code = k,target_info = v,last_hold_by_code = last_hold_by_code)


    def run(self,datetime,stock_pool,stock_rank,total_position):
        last_account_dict = self.bookkeeper.lastAccountState()
        target_hold_dict = self.position_spilitor.getPosition(stock_pool,stock_rank,total_position,last_account_dict)
        self.bookkeeper.updateAccountInfo(target_hold_dict)
        self.tradeByDatetime(last_account_dict,target_hold_dict)

        
        