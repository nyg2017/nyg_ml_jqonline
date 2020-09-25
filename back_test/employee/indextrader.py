import pandas as pd
import numpy as np
import os

class IndexTrader(object):
    def __init__(self,index_code,start_date ,bookkeeper):
        self.index = index_code
        self.bookkeeper = bookkeeper
        init_index_value = self.getIndexValue(index_code,start_date)
        self.bookkeeper.addNewIndexState(index_code = index_code,index_value = init_index_value)

    def run(self,date_time):
        pass

    def getIndexValue(self,index_code,start_date):
        return 9123.0