import sys
if __name__ == "__main__":
    sys.path.append("../nyg_ml_jqonline")

import numpy as np
import pandas as pd
import jqdatasdk as jq
from online_creator.label_creator.daily_label.daily_price import DailyPrice
from util.jqdata_processor import dateArr2List,list2Dic,invert_dict


label_creator_dic = {
    "p":DailyPrice,
}

def init_label_list(feature_cfg):
    re_list = []
    for key in feature_cfg.keys():
        re_list.append(label_creator_dic[key](feature_cfg[key],key))
    return re_list


class Label(object):
    def __init__(self,feature_cfg,UserDataApi,early_date = "2020-01-01",last_date = "2020-11-30"):
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
            print ("processing label:",date)
            daily_label_info = self.creatLabelByDate(date,stock_list)
            self.label_dict["label_all"][date] = daily_label_info
            # self.label_dict["label_all"][date]["info"] = daily_label
            # self.label_dict["label_all"][date]["valid_index"] = valid_index

        return self.label_dict

    def creatLabelByDate(self,date,stock_list):
        label = dict()
        for creator in self.label_creator_list:
            label_temp , label_name = creator.getLabelByDate(date,stock_list,self.date_index_dict,self.inverse_date_index_dict,self.UserDataApi)

            label[label_name] = label_temp
        valid_index = self.UserDataApi.getSuspensionInfor(date,stock_list)

        daily_label_info = {"info":label,"valid_index":valid_index}
        return daily_label_info

    def creatDailyLabel(self,date,stock_list):
        daily_label_dict = dict()
        daily_label_dict["label_all"] = dict()
        daily_label_dict["label_all"][date] = self.creatLabelByDate(date,stock_list)
        daily_label_dict["date_index"] = {0:date}
        return daily_label_dict

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