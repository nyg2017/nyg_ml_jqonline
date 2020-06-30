import sys
if __name__ == "__main__":
    sys.path.append("/Users/tall100/github/nyg_ml_jqonline")

import numpy as np
import pandas as pd
import jqdatasdk as jq
from online_creator.feature_creator.daily_feature.daily_price_feature import DailyPriceFeature
from online_creator.feature_creator.daily_feature.daily_volume_feature import DailyVolumeFeature
from util.jqdata_processor import dateArr2List,list2Dic,invert_dict



feature_creator_dic = {
    "p":DailyPriceFeature,
    "v":DailyVolumeFeature
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
        self.feature_creator_list = init_feature_list(self.cfg["feature_cfg"])
        self.initDateIndexDict(early_date)
    

    def initDateIndexDict(self,early_date):

        trade_date_arr = jq.get_trade_days(early_date,self.end_date)
        self.trade_date_list = dateArr2List(trade_date_arr)
        self.date_index_dict = list2Dic(self.trade_date_list)
        self.inverse_date_index_dict = invert_dict(self.date_index_dict )

        self.date_list = dateArr2List(jq.get_trade_days(self.start_date,self.end_date))

    def createFeatureAll(self):

        feature_all = []
        for date in self.date_list:
            daily_feature = self.creatFeatureByDate(date)
            print(len(daily_feature))
            feature_all.append(daily_feature)

        return feature_all

    
    def creatFeatureByDate(self,date):
        feature = []
        for creator in self.feature_creator_list:
            feature = feature + creator.getFeatureByDate(date,self.stock_list,self.date_index_dict,self.inverse_date_index_dict)

        return feature

    def checkFeature():
        for creator in self.feature_creator_list:
            creator.check(self.start_date)


if __name__ == "__main__":
    import json
    from util.jq_init import login
    login()
    with open("./DATA/ori_data/industry_list/sw_l3.json","r") as f:
        industry_list = json.load(f)

    feature_cfg = "./config/feature_create_cfg.json"
    with open(feature_cfg,"r") as f:
        feature_cfg = json.load(f)

    stock_list = industry_list["L72"]["stocks_list"]

    f = Feature(feature_cfg,stock_list)
    f.createFeatureAll()