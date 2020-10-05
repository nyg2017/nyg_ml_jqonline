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


UserDataApi.login()
buffered_feature = True



def predict(train_cfg):
    with open(train_cfg,"r") as f:
        train_cfg = json.load(f)

    feature_cfg = train_cfg["feature_cfg"]
    model_name = train_cfg["model"]
    model_cfg = train_cfg["model_cfg"]

    #feature_cfg = "./config/feature_create_cfg.json"
    with open(feature_cfg,"r") as f:
        feature_cfg = json.load(f)

    stock_list = jq.get_industry_stocks('I64')
    feature_creator = Feature(feature_cfg,stock_list)
    #label_creator = Label(feature_cfg,stock_list)
    model = restore_model_from_file(model_name,model_cfg)

    if not buffered_feature:
        feature = []
        label = []
        for date in feature_creator.date_list:
            print ("creating feature, date:",date)
            feature_per_day = feature_creator.creatFeatureByDate(date)
            feature.append(feature_per_day)

        feature = np.array(feature).reshape(-1,feature[0].shape[-1])
        print (feature.shape)
        np.save("./DATA/buffer/feature_for_prediction.npy",feature)
    else:
        feature = np.load("./DATA/buffer/feature_for_prediction.npy")



    y = model.predict(feature)
    print (y)


if __name__ == "__main__":
    
    train_cfg = "./config/train_cfg.json"
    predict(train_cfg)