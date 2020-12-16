import numpy as np
import pandas as pd
import json
from feature_engine.base_feature_engine import BaseFeatureEngine



class LgbFeatureEngine(BaseFeatureEngine):
    def __init__(self, cfg):  # 可调用name属性
        # super(Class, self).method()
        super(LgbFeatureEngine, self).__init__(cfg)

    def initOperation(self,cfg):
        op_list = []
        for key in cfg.keys():
            op_list.append(self.operation_dic[key](cfg[key]))
        
        return op_list