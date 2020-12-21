import sys
sys.path.append("../nyg_ml_jqonline")
from model.build_model import build_model,restore_model_from_file
from online_creator.feature import Feature
from online_creator.label import Label
import json
import numpy as np
from data_interface.data_api import UserDataApi
#from .fixes import _object_dtype_isnan
import jqdatasdk as jq
from feature_engine.feature_engine_build import build_feature_engine

buffered_feature = False




def create_feature(feature_cfg):
    UserDataApi_ = UserDataApi()
    stock_list = jq.get_industry_stocks('I64')
    print (stock_list)
    feature_creator = Feature(feature_cfg,UserDataApi_)
    label_creator = Label(feature_cfg,UserDataApi_)
    
    feature_dict = feature_creator.createFeatureAll(stock_list)
    label_dict = label_creator.createLabelAll(stock_list)
    feature_enginer = build_feature_engine("lgb",feature_cfg["engine_cfg"])

    info_dict = {
        "feature":feature_dict,
        "label":label_dict
    }
    info_dict = feature_enginer.run(info_dict)
    #print (feature,label)


def create_feature_daily(feature_cfg):
    UserDataApi_ = UserDataApi()
    stock_list = jq.get_industry_stocks('I64')
    feature_creator = Feature(feature_cfg,UserDataApi_)
    label_creator = Label(feature_cfg,UserDataApi_)
    feature_enginer = build_feature_engine("lgb",feature_cfg["engine_cfg"])


    start_date = feature_cfg["start"]
    end_date = feature_cfg["end"]

    for date in UserDataApi_.getTradeDays(start_date = start_date,end_date = end_date):
        daily_feature_info = feature_creator.creatDailyFeature(date,stock_list)
        daily_label_info = label_creator.creatDailyLabel(date,stock_list)
        info_dict = {"feature":daily_feature_info,"label":None}
        info_dict = feature_enginer.run_test(info_dict)
        print (info_dict.keys(),info_dict["feature"].shape,info_dict["re_feature_valid_index"].shape)



if __name__ == "__main__":
    import json
    from util.jq_init import login
    login()
    
    feature_cfg = "./config/feature_create_cfg.json"
    with open(feature_cfg,"r") as f:
        feature_cfg = json.load(f)
    
    create_feature_daily(feature_cfg)