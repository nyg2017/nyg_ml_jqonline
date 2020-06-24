import numpy as np
import pandas as pd
import jqdatasdk as jq


feature_creator_dic = {
    "":""
}

def init_feature_list(feature_cfg):
    re_list = []
    for key in feature_cfg.keys():
        re_list.append(feature_creator_dic[key](feature_cfg[key]))
    return re_list


class Feature(object):
    def __init__(self,feature_cfg,stock_list,early_date = "2010-10-10"):
        self.cfg = feature_cfg
        self.stock_list = stock_list
        self.start_date = self.cfg['start']
        self.end_date = self.cfg['end']
        self.feature_creator_list = init_feature_list(self.cfg)
        self.initDateIndexDict(early_date)
    

   def initDateIndexDict(self,early_date):

        trade_date_arr = jq.get_trade_days(early_date,self.end_date)
        self.trade_date_list = dateArr2List(trade_date_arr)
        self.date_index_dict = list2Dic(self.trade_date_list)
        #self.inverse_date_index_dict =  invert_dict(self.date_index_dict )


    def createFeatureAll(self):

        feature_all = []
        for date in self.trade_date_list:
            daily_feature = creatFeatureByDate(date)
            feature_all.append(daily_feature)
        
        return feature_all

    
    def creatFeatureByDate(self,date):
        feature = []
        for creator in self.feature_creator_list:
            feature.append(creator.getFeatureByDate(date,self.stock_list,self.date_index_dict))

        return feature

    def checkFeature():
        for creator in self.feature_creator_list:
            creator.check(self.start_date)