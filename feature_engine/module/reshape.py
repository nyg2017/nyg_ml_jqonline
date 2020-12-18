from feature_engine.module.base_module import BaseModule
import numpy as np

class Reshape(BaseModule):

    def __init__(self, cfg):  # 可调用name属性
        # super(Class, self).method()
        super(Reshape, self).__init__(cfg)


    def extractDailyFetureLabel(self,daily_feature_dic):
        daily_feature = []
        for k ,v in daily_feature_dic["info"].items():
            for k_,v_ in v.items():
                daily_feature.append(v_)
            
        daily_feature = np.concatenate(tuple(daily_feature),axis = -1)
        daily_valid_index = daily_feature_dic["valid_index"]
        return daily_feature ,daily_valid_index

    def valid_filter_value(self,arr_1,index,value = "nan"):
        #print (arr_1[~index])
        if value == "nan":
            value = np.nan

        arr_1[~index] = value
        return arr_1

    def run(self,info_dict):
        feature = info_dict["feature"]
        if "label" not in info_dict.keys():
            label = None
        else:
            label = info_dict["label"]
        re_feature = []
        re_feature_valid_index =[]
        feature_date_key_index = feature["date_index"]
        for index,date in feature_date_key_index.items():
            daily_feature, daily_valid_index = self.extractDailyFetureLabel(feature["feature_all"][date])
            re_feature.append(daily_feature)
            re_feature_valid_index.append(daily_valid_index)
        
        re_feature = np.array(re_feature)
        re_feature_valid_index = np.array(re_feature_valid_index)
        #re_feature = self.valid_filter_value(re_feature,re_feature_valid_index,self.cfg["valid_filter_value"])

        if not (label is None):
            re_label = []
            re_label_valid_index = []
            label_date_key_index = label["date_index"]
            assert feature_date_key_index == label_date_key_index ,print ("date index error")
            for index,date in label_date_key_index.items():
                daily_label, daily_valid_index = self.extractDailyFetureLabel(label["label_all"][date])
                re_label.append(daily_label)
                re_label_valid_index.append(daily_valid_index)


            re_label = np.array(re_label)
            re_label_valid_index = np.array(re_label_valid_index)
            #re_label = self.valid_filter_value(re_label,re_label_valid_index,self.cfg["valid_filter_value"])

 
        if self.cfg["main_dim"] == "stock":
            re_feature = np.transpose(re_feature,(1,0,2))
            re_feature_valid_index = np.transpose(re_feature_valid_index,(1,0))
            if not (label is None):
                re_label = np.transpose(re_label,(1,0,2))
                re_label_valid_index = np.transpose(re_label_valid_index,(1,0))

            else:
                re_label = None
                re_label_valid_index = None
        
        re_info_dict = {
            "feature":re_feature,
            "label":re_label,
            "re_feature_valid_index":re_feature_valid_index,
            "re_label_valid_index":re_label_valid_index
        }
        return re_info_dict