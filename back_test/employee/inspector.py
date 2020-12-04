import numpy as np


class Inspector(object):
    def __init__(self,UserDataApi):
        self.UserDataApi = UserDataApi
        

    def suspensionCheck(self,date_time,stock_code_list):
        suspension = self.UserDataApi.getSuspensionInfor(date_time,stock_code_list)
        return np.array(suspension)

    def limitCheck(self,date_time,stock_code_list):
        limit = self.UserDataApi.getLimitInfor(date_time,stock_code_list)
        return np.array(limit)

    def tradeableCheck(self,date_time,stock_code_list):
        suspension = self.suspensionCheck(date_time,stock_code_list)
        limit = self.limitCheck(date_time,stock_code_list)
        tradeable = np.logical_and(suspension,limit)
        return tradeable
        #return stock_list[tradeable],stock_rank[tradeable]

