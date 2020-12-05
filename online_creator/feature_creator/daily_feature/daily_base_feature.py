
import os
import numpy as np


class DailyFeatureBase(object):
    def __init__(self,cfg,key):
        self.cfg = cfg
        self.name = key
    
    def getFeatureByDate(self,date,stock_list,date_index_dict):

        pass
    
    def groupOp(self,feature,didx):
        pass

    def check(self,didx,inst_idx):
        pass  