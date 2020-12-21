import numpy as np
import pandas as pd
import json
from feature_engine.base_feature_engine import BaseFeatureEngine



class LgbFeatureEngine(BaseFeatureEngine):
    def __init__(self, cfg):  # 可调用name属性
        # super(Class, self).method()
        self.key_list = ["reshape","nan_to_num","clip"]
        super(LgbFeatureEngine, self).__init__(cfg)
        


    def initOperation(self,cfg):
        op_list = []
        for key in self.key_list:
            op_list.append(self.operation_dic[key](cfg[key]))
        return op_list

    
    def post_process(self,info_dict, train_test = "train"):
        feature = info_dict["feature"]
        label = info_dict["label"]
        re_feature_valid_index = info_dict["re_feature_valid_index"]
        re_label_valid_index = info_dict["re_label_valid_index"]

        feature = feature.reshape(-1,feature.shape[-1])
        re_feature_valid_index = re_feature_valid_index.reshape(-1)
        #feature = feature[re_feature_valid_index]
        if not (label is None):
            label_clip_index = info_dict["label_clip_index"]
            label[label_clip_index] = 0.0
            label = label.reshape(-1,label.shape[-1])
            re_label_valid_index = re_label_valid_index.reshape(-1)
            #label = label[re_label_valid_index]
            assert feature.shape[0] == label.shape[0]

        if train_test == "train":
            feature = feature[re_feature_valid_index]
            label = label[re_label_valid_index]
        

        info_dict["feature"] = feature
        info_dict["label"] = label

        
        return info_dict