import numpy as np
import os
import pandas as pd
from back_test.util.position import *
from date_interface.jq_data import getClosePrices


position_func_dict = {
    "mean":meanPosition
}


'''
    "target_hold_dict":{
        "target_code":{
            "market_price":3414,
            "target_num":1234,
            "target_percent":0.123
        }
    }
'''

class PositionSpilitor(object):
    def __init__(self,mode,bookkeeper):
        self.mode = mode
        self.position_func = position_func_dict[self.mode]
        self.bookkeeper = bookkeeper

    
    def initTargetHoldDict(self,stock_pool,position_percent,last_hold_state):
        target_hold_dict = dict()
        for i,stock_code in enumerate(stock_pool):
            temp_dict = dict()
            temp_dict['target_percent'] = position_percent[i]
            target_hold_dict[stock_code] = temp_dict
        
        for k in last_hold_state.keys():
            if k not in stock_pool:
                temp_dict = dict()
                temp_dict['target_percent'] = 0.0
                target_hold_dict[stock_code] = temp_dict  

        return target_hold_dict              
    
    def calculateTargetNum(self,tradeable_capital,target_percent,price,mini_tradeable_unit = 100):
        return  (tradeable_capital * target_percent) // (price * mini_tradeable_unit) * 100
    
    def calculateTargetHoldDict(self,stock_price_dict,tradeable_capital,inited_percent_target_hold_dict):



        for i,code in enumerate(stock_price_dict.keys()):
            inited_percent_target_hold_dict[code]['market_price'] = stock_price_dict[code]
            inited_percent_target_hold_dict[code]['target_num'] = self.calculateTargetNum(tradeable_capital,inited_percent_target_hold_dict[code]['target_percent'],stock_price_dict[code])

        return inited_percent_target_hold_dict



    def getTargetPosition(self,stock_price_dict,stock_pool,stock_rank,total_position,last_hold_account_dict):
        #ori_hold_account_dict['capital']
        capital = self.bookkeeper.capital
        tradeable_capital = total_position * capital

        position_percent = self.position_func(stock_rank)
        
        last_hold_state = last_hold_account_dict['hold_state']
        
        inited_percent_target_hold_dict = self.initTargetHoldDict(stock_pool,position_percent,last_hold_state)

        target_hold_dict = self.calculateTargetHoldDict(stock_price_dict,tradeable_capital,inited_percent_target_hold_dict)
        

        return target_hold_dict