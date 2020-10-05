import sys
sys.path.append("../nyg_ml_jqonline")
from model.build_model import build_model,restore_model_from_file
from online_creator.feature import Feature
from online_creator.label import Label
import json
import numpy as np
from date_interface.data_api import UserDataApi
#from .fixes import _object_dtype_isnan
import jqdatasdk as jq
from back_test.base_bt import BaseBT


UserDataApi.login()
buffered_feature = True



def initBackTest(start_date,end_date):
    capital = 1000000
    base_index = '000001.XSHG'
    weight_mode = "mean"
    fee_rate = 0.00005
    slide_point = 0.01
    start_date = "2020-07-03"
    end_date = "2020-07-13"
    trade_mode = "mean"
    total_position = 0.95
    bt = BaseBT(capital,base_index,weight_mode,fee_rate,slide_point,start_date,end_date,trade_mode)
    return bt

def predictBacktest(train_cfg):
    with open(train_cfg,"r") as f:
        train_cfg = json.load(f)

    
    feature_cfg = train_cfg["feature_cfg"]
    model_name = train_cfg["model"]
    model_cfg = train_cfg["model_cfg"]


    #feature_cfg = "./config/feature_create_cfg.json"
    with open(feature_cfg,"r") as f:
        feature_cfg = json.load(f)
    bt = initBackTest(feature_cfg['start'],feature_cfg['end'])

    stock_list = jq.get_industry_stocks('I64')
    feature_creator = Feature(feature_cfg,stock_list)
    #label_creator = Label(feature_cfg,stock_list)
    model = restore_model_from_file(model_name,model_cfg)

    if not buffered_feature:
        feature_dic = dict()
        for date in feature_creator.date_list:
            print ("creating feature, date:",date)
            feature_per_day = feature_creator.creatFeatureByDate(date)
            feature_dic[date] = feature_per_day

        np.save("./DATA/buffer/feature_for_back_test.npy",feature_dic)
    else:
        feature_dic = np.load("./DATA/buffer/feature_for_back_test.npy").item()
        #print (feature_dic)

    for k ,v in feature_dic.items():
        rank = np.zeros(len(stock_list))
        bt.run(k,stock_list,rank,0.9)
        print (bt.bookkeeper.capital)

if __name__ == "__main__":
    
    train_cfg = "./config/train_cfg.json"
    predictBacktest(train_cfg)