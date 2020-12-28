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
from back_test.base_bt import BaseBT
from sample.create_feature import create_feature_daily
from feature_engine.feature_engine_build import build_feature_engine
from util.jq_init import login
login()


buffered_feature = True
start_date = '2019-07-01'
end_date = '2019-12-31'

def initBackTest(start_date,end_date,UserDataApi):
    capital = 1000000
    base_index = '000300.XSHG'
    fee_rate = 0.0005
    slide_point = 0.01
    start_date = start_date
    end_date = end_date
    position_mode = "exp"
    total_position = 1.00
    bt = BaseBT(capital,base_index,fee_rate,slide_point,start_date,end_date,position_mode,UserDataApi)
    return bt

def predictBacktest(train_cfg):
    UserDataApi_ = UserDataApi()
    with open(train_cfg,"r") as f:
        train_cfg = json.load(f)

    
    feature_cfg = train_cfg["feature_cfg"]
    model_name = train_cfg["model"]
    model_cfg = train_cfg["model_cfg"]


    #feature_cfg = "./config/feature_create_cfg.json"
    with open(feature_cfg,"r") as f:
        feature_cfg = json.load(f)

    test_start = feature_cfg['test_start']
    test_end = feature_cfg['test_end']

    print (feature_cfg)
    stock_list = jq.get_index_stocks('000300.XSHG')
    stock_array = np.array(stock_list)
    feature_creator = Feature(feature_cfg,UserDataApi_)
    label_creator = Label(feature_cfg,UserDataApi_)
    model = restore_model_from_file(model_name,model_cfg)

    date_list = UserDataApi_.getTradeDays(test_start,test_end)
    bt = initBackTest(date_list[0],date_list[-1],UserDataApi_)
    feature_enginer = build_feature_engine("lgb",feature_cfg["engine_cfg"])
    
    

    for date in date_list:
        info = create_feature_daily(date,stock_list,feature_creator,label_creator,feature_enginer,UserDataApi_)        
        feature_per_day = info["feature"]
        label_per_day = info["label"]
        prediction = model.predict(feature_per_day)
        v = UserDataApi_.validIndex(date,stock_list)
        stock_list_temp = np.array(stock_list)[v]
        prediction = prediction[v]
        
        #prediction = label_per_day[0,:,0][v]
        prediction = np.nan_to_num(prediction)
        #v =  ~(prediction == prediction_)
        #prediction[v] = 0.0
        #index = prediction > aver
        #stock_list_temp = stock_list_temp[index]
        #prediction = prediction[index]
        bt.run(date,stock_list_temp,prediction,0.9)
        print ("date:",date,"capital:",bt.bookkeeper.capital)
        # if date == "2020-03-11":
        #     print (prediction)
        #     exit()
    if not buffered_feature:
        np.save("./DATA/buffer/feature_for_prediction.npy",feature_dic)

    bt.analysist()
    bt.vis()

if __name__ == "__main__":
    
    train_cfg = "./config/train_cfg.json"
    predictBacktest(train_cfg)