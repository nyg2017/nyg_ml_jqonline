import pandas as pd
import numpy as np
import os



class IndexTrader(object):
    def __init__(self,index_code,start_date ,bookkeeper,UserDataApi):
        self.UserDataApi = UserDataApi
        self.index_code = index_code
        self.bookkeeper = bookkeeper
        init_index_value = self.UserDataApi.getIndexValue(start_date,self.index_code)

        if len(init_index_value) == 0:
            init_index_value = -1
        self.bookkeeper.addNewIndexState(index_code = self.index_code,index_value = init_index_value)

    def run(self,date_time):
        index_value = self.UserDataApi.getIndexValue(date_time,self.index_code)
        self.bookkeeper.addNewIndexState(index_code = self.index_code,index_value = index_value)

