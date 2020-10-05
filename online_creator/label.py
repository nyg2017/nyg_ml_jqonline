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
        re_list.append(label_creator_dic[key](feature_cfg[key]))
    return re_list


class Label(object):
    def __init__(self,feature_cfg,stock_list,early_date = "2010-10-10",last_date = "2020-10-10"):
        self.cfg = feature_cfg
        self.stock_list = stock_list
        self.start_date = self.cfg['start']
        self.end_date = self.cfg['end']
        self.label_creator_list = init_label_list(self.cfg["label_cfg"])
        self.initDateIndexDict(early_date,last_date)
    

    def initDateIndexDict(self,early_date,last_date):

        trade_date_arr = jq.get_trade_days(early_date,last_date)
        self.trade_date_list = dateArr2List(trade_date_arr)
        self.date_index_dict = list2Dic(self.trade_date_list)
        self.inverse_date_index_dict = invert_dict(self.date_index_dict )

        self.date_list = dateArr2List(jq.get_trade_days(self.start_date,self.end_date))

    def createLabelAll(self):

        label_all = []
        for date in self.date_list:
            daily_label = self.creatLabelByDate(date)
            label_all.append(np.array(daily_label))

        return np.concatenate(tuple(label_all),axis= 0)

    # def createBatch(self,idx_list):
    #     for idx in idx_list:
    #         daily_feature = self.creatLabelByDate(date)
            
    #         feature_all.append(daily_feature)
        
    #     return np.concatenate(tuple(feature_all),axis= 0)
    
    def creatLabelByDate(self,date):
        label = []
        for creator in self.label_creator_list:
            label_temp = creator.getLabelByDate(date,self.stock_list,self.date_index_dict,self.inverse_date_index_dict)
            
            label_temp = np.concatenate(tuple(label_temp),axis = -1)
            label.append(label_temp)

        return np.concatenate(tuple(label),axis = 0)

    def checkLabel():
        for creator in self.label_creator_list:
            creator.check(self.start_date)


if __name__ == "__main__":
    import json
    from util.jq_init import login
    login()


    feature_cfg = "./config/feature_create_cfg.json"
    with open(feature_cfg,"r") as f:
        feature_cfg = json.load(f)

    stock_list = jq.get_industry_stocks('I64')

    f = Label(feature_cfg,stock_list)
    label_all = f.createLabelAll()
    print (label_all.shape)