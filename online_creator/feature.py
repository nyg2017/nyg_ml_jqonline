import sys
if __name__ == "__main__":
    sys.path.append("../nyg_ml_jqonline")

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
        re_list.append(feature_creator_dic[key](feature_cfg[key],key))
    return re_list


class Feature(object):
    def __init__(self,feature_cfg,UserDataApi,early_date = "2020-01-01",last_date = "2020-11-30"):
        self.cfg = feature_cfg
        #self.stock_list = stock_list
        self.UserDataApi = UserDataApi
        self.start_date = self.cfg['start']
        self.end_date = self.cfg['end']
        self.feature_creator_list = init_feature_list(self.cfg["feature_cfg"])
        self.feature_dict = dict()
        self.feature_dict["cfg"] = self.cfg
        self.initDateIndexDict(early_date,last_date)
    

    def initDateIndexDict(self,early_date,last_date):
        #pri)nt (early_date,last_date
        self.trade_date_list = self.UserDataApi.getTradeDays(early_date,last_date)
        self.date_index_dict = list2Dic(self.trade_date_list)
        self.inverse_date_index_dict = invert_dict(self.date_index_dict )

        self.date_list = self.UserDataApi.getTradeDays(self.start_date,self.end_date)
        self.feature_dict["date_index"] = dict(zip([i for i in range(len(self.date_list))],self.date_list))

    def createFeatureAll(self,stock_list):

        self.feature_dict["feature_all"] = dict()
        for date in self.date_list:
            daily_feature = self.creatFeatureByDate(date,stock_list)
            self.feature_dict["feature_all"][date] = dict()
            self.feature_dict["feature_all"][date]["info"] = daily_feature
            self.feature_dict["feature_all"][date]["valid_index"] = self.UserDataApi.getSuspensionInfor(date,stock_list)
        
        return self.feature_dict

    def creatFeatureByDate(self,date,stock_list):
        feature = dict()
        for creator in self.feature_creator_list:
            feature_temp,feature_name = creator.getFeatureByDate(date,stock_list,self.date_index_dict,self.inverse_date_index_dict,self.UserDataApi)
            feature[feature_name] = feature_temp
     
        return feature

    def checkFeature():
        for creator in self.feature_creator_list:
            creator.check(self.start_date)


if __name__ == "__main__":
    import json
    from util.jq_init import login
    login()
    from data_interface.data_api import UserDataApi
    UserDataApi = UserDataApi()
    feature_cfg = "./config/feature_create_cfg.json"
    with open(feature_cfg,"r") as f:
        feature_cfg = json.load(f)

    stock_list = jq.get_industry_stocks('I64')

    f = Feature(feature_cfg,UserDataApi)
    f.createFeatureAll(stock_list)
    b = f.feature_dict["feature_all"]["2020-02-07"]["p"]["var"]
    r = f.feature_dict["feature_all"]["2020-02-07"]["p"]["return"]
    r = f.feature_dict["feature_all"]["2020-02-07"]["p"]["high_d_close"]

    
    print (type(b),b.shape,r.shape)