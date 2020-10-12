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
start_date = '2019-07-01'
end_date = '2019-07-05'

def initBackTest(start_date,end_date):
    capital = 1000000
    base_index = '000001.XSHG'
    fee_rate = 0.0005
    slide_point = 0.01
    start_date = start_date
    end_date = end_date
    position_mode = "exp"
    total_position = 0.95
    bt = BaseBT(capital,base_index,fee_rate,slide_point,start_date,end_date,position_mode)
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

    feature_cfg['start'] = start_date
    feature_cfg['end'] = end_date
    bt = initBackTest(feature_cfg['start'],feature_cfg['end'])

    print (feature_cfg)
    stock_list = jq.get_industry_stocks('I64')
    feature_creator = Feature(feature_cfg,stock_list)
    #label_creator = Label(feature_cfg,stock_list)
    model = restore_model_from_file(model_name,model_cfg)

    
    if buffered_feature:
        feature_dic = np.load("./DATA/buffer/feature_for_prediction.npy").item()
    else:
        feature_dic = dict()
    for date in feature_creator.date_list:
        print ("predicting feature, date:",date)
        if buffered_feature:
            feature_per_day = feature_dic[date]
        else:
            feature_per_day = feature_creator.creatFeatureByDate(date)
            feature_dic[date] = feature_per_day
        
        prediction = model.predict(feature_per_day)
        v = UserDataApi.validIndex(date,stock_list)
        stock_list_temp = np.array(stock_list)[v]
        prediction = prediction[v]
        aver = np.argmax(prediction)
        #index = prediction > aver
        #stock_list_temp = stock_list_temp[index]
        #prediction = prediction[index]
        bt.run(date,stock_list_temp,prediction,0.9)
        print ("capital:",bt.bookkeeper.capital)
    if not buffered_feature:
        np.save("./DATA/buffer/feature_for_prediction.npy",feature_dic)

    bt.analysist()
    bt.vis()

if __name__ == "__main__":
    
    train_cfg = "./config/train_cfg.json"
    predictBacktest(train_cfg)