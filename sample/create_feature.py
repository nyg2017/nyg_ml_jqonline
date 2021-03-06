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
buffer_feature_path = "/home/tal100/github/data/feature.pkl"



import pickle

def save_obj(obj, path ):
    with open(path, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(path ):
    with open(path, 'rb') as f:
        return pickle.load(f)

def create_feature(feature_cfg,stock_list,if_dump = False,load_feature = False):
    if load_feature:
        return load_obj(buffer_feature_path)

    UserDataApi_ = UserDataApi()
    
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
    if if_dump == True:
        save_obj(info_dict,buffer_feature_path)
    return info_dict
    #print (feature,label)


# def create_feature_daily(feature_cfg,stock_list,UserDataApi_):
#     feature_creator = Feature(feature_cfg,UserDataApi_)
#     label_creator = Label(feature_cfg,UserDataApi_)
#     feature_enginer = build_feature_engine("lgb",feature_cfg["engine_cfg"])


#     start_date = feature_cfg["start"]
#     end_date = feature_cfg["end"]

#     for date in UserDataApi_.getTradeDays(start_date = start_date,end_date = end_date):
#         daily_feature_info = feature_creator.creatDailyFeature(date,stock_list)
#         daily_label_info = label_creator.creatDailyLabel(date,stock_list)
#         info_dict = {"feature":daily_feature_info,"label":None}
#         info_dict = feature_enginer.run_test(info_dict)
#         print (info_dict.keys(),info_dict["feature"].shape,info_dict["re_feature_valid_index"].shape)


def create_feature_daily(date,stock_list,feature_creator,label_creator,feature_enginer,UserDataApi):
    daily_feature_info = feature_creator.creatDailyFeature(date,stock_list)
    daily_label_info = label_creator.creatDailyLabel(date,stock_list)
    info_dict = {"feature":daily_feature_info,"label":daily_label_info}
    info_dict = feature_enginer.run_test(info_dict)
    return info_dict
    #print (info_dict.keys(),info_dict["feature"].shape,info_dict["re_feature_valid_index"].shape)



if __name__ == "__main__":
    import json
    from util.jq_init import login
    login()
    
    feature_cfg = "./config/feature_create_cfg.json"
    with open(feature_cfg,"r") as f:
        feature_cfg = json.load(f)
    stock_list = jq.get_industry_stocks('I64')

    create_feature_daily(feature_cfg,stock_list)