import sys
sys.path.append("../nyg_ml_jqonline")
from model.build_model import build_model
from online_creator.feature import Feature
import json
from util.jq_init import login
import numpy as np
#from .fixes import _object_dtype_isnan

login()


def train(train_cfg):
    with open(train_cfg,"r") as f:
        train_cfg = json.load(f)

    feature_cfg = train_cfg["feature_cfg"]
    model_name = train_cfg["model"]
    model_cfg = train_cfg["model_cfg"]
    #print (model_cfg)
    with open("./DATA/ori_data/industry_list/sw_l3.json","r") as f:
        industry_list = json.load(f)

    feature_cfg = "./config/feature_create_cfg.json"
    with open(feature_cfg,"r") as f:
        feature_cfg = json.load(f)

    stock_list = industry_list["L72"]["stocks_list"]

    feature_creator = Feature(feature_cfg,stock_list)

    model = build_model(model_name,model_cfg)

    feature_all = np.array(feature_creator.createFeatureAll())
    #print (model)
    
    feature_all = np.nan_to_num(feature_all)
    label = feature_all[:,-1]
    #print (label)
    #label = np.array([np.nan])
    print (np.isnan(label),label,type(label),np.nan_to_num(label))
    print (label<1)
    #print (feature_all.shape)
    model.fit(feature_all,label)


if __name__ == "__main__":
    
    trian_cfg = "./config/train_cfg.json"
    train(trian_cfg)