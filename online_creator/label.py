import sys
if __name__ == "__main__":
    sys.path.append("../nyg_ml_jqonline")

import numpy as np
import pandas as pd
import jqdatasdk as jq
from online_creator.label_creator.daily_label.daily_return import DailyReturn
from util.jqdata_processor import dateArr2List,list2Dic,invert_dict


label_creator_dic = {
    "return":DailyReturn,
}

def init_label_list(feature_cfg):
    re_list = []
    for key in feature_cfg.keys():
        re_list.append(label_creator_dic[key](key,feature_cfg[key]))
    return re_list


class Label(object):
    def __init__(self,feature_cfg,UserDataApi,early_date = "2010-10-10",last_date = "2020-10-10"):
        self.cfg = feature_cfg
        #self.stock_list = stock_list
        self.UserDataApi = UserDataApi
        self.start_date = self.cfg['start']
        self.end_date = self.cfg['end']
        self.label_creator_list = init_label_list(self.cfg["label_cfg"])
        self.label_dict = dict()
        self.initDateIndexDict(early_date,last_date)

    def initDateIndexDict(self,early_date,last_date):
        self.trade_date_list = self.UserDataApi.getTradeDays(early_date,last_date)
        self.date_index_dict = list2Dic(self.trade_date_list)
        self.inverse_date_index_dict = invert_dict(self.date_index_dict )

        self.date_list = self.UserDataApi.getTradeDays(self.start_date,self.end_date)
        self.label_dict["date_index"] = dict(zip([i for i in range(len(self.date_list))],self.date_list))

    def createLabelAll(self,stock_list):

        self.label_dict["label_all"] = dict()
        for date in self.date_list:
            daily_label = self.creatLabelByDate(date,stock_list)
            self.label_dict["label_all"][date] = daily_label
            self.label_dict["label_all"][date]["valid_index"] = self.UserDataApi.getSuspensionInfor(date,stock_list)

        return self.label_dict
    # def createBatch(self,idx_list):
    #     for idx in idx_list:
    #         daily_feature = self.creatLabelByDate(date)
            
    #         feature_all.append(daily_feature)
        
    #     return np.concatenate(tuple(feature_all),axis= 0)
    
    def creatLabelByDate(self,date,stock_list):
        label = dict()
        for creator in self.label_creator_list:
            label_temp , label_name = creator.getLabelByDate(date,stock_list,self.date_index_dict,self.inverse_date_index_dict,self.UserDataApi)
            label[label_name] = label_temp
        return label

    def checkLabel():
        for creator in self.label_creator_list:
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

    f = Label(feature_cfg,UserDataApi)
    label_all = f.createLabelAll(stock_list)
    print (label_all["label_all"]["2020-03-04"]["valid_index"])