import numpy as np
import os

class DailyLabelBase(object):

    def __init__(self,cfg,key):
        self.cfg = cfg
        self.name = key
        pass

    def getFeatureByDate(self,date,stock_list,date_index_dict):

        pass
    
    def groupOp(self,feature,didx):
        pass

    def check(self,didx,inst_idx):
        pass  