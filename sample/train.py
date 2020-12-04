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

buffered_feature = False

def train(train_cfg):
    with open(train_cfg,"r") as f:
        train_cfg = json.load(f)

    UserDataApi = UserDataApi()
    feature_cfg = train_cfg["feature_cfg"]
    model_name = train_cfg["model"]
    model_cfg = train_cfg["model_cfg"]

    #feature_cfg = "./config/feature_create_cfg.json"
    with open(feature_cfg,"r") as f:
        feature_cfg = json.load(f)

    
    #print (stock_array)

    feature_creator = Feature(feature_cfg,UserDataApi)
    label_creator = Label(feature_cfg,UserDataApi)
    model = build_model(model_name,model_cfg)

    if not buffered_feature:
        feature = []
        label = []
        for date in feature_creator.date_list:
            print ("creating feature and label, date:",date)
            stock_array = np.array(jq.get_index_stocks('000001.XSHG',date = date))
            is_public = UserDataApi.isPublic(date,stock_array)

            stock_array_temp = stock_array[is_public]

            feature_per_day = feature_creator.creatFeatureByDate(date,stock_array_temp)
            label_per_day = label_creator.creatLabelByDate(date,stock_array_temp)
            feature.append(feature_per_day)
            label.append(label_per_day)

        feature = np.concatenate(tuple(feature),axis = 0).reshape(-1,feature[0].shape[-1])
        label = np.concatenate(tuple(label),axis = 0).reshape(-1,label[0].shape[-1])
        np.save("./DATA/buffer/feature_.npy",feature)
        np.save("./DATA/buffer/label_.npy",label)
    else:
        feature = np.load("./DATA/buffer/feature.npy")
        label = np.load("./DATA/buffer/label.npy")


    

    label_ = np.nan_to_num(label.astype(np.float))
    v = (label_ == label).reshape(-1)
    feature = feature[v]
    label = label[v]

    v = (np.abs(label) > 0.015).reshape(-1)
    print (v)
    label = label[v]
    feature = feature[v]

    model.fit(feature,label)
    model.dump()




if __name__ == "__main__":
    
    trian_cfg = "./config/train_cfg.json"
    train(trian_cfg)
