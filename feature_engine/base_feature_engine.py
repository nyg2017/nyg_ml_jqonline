import numpy as np
import pandas as pd
import json
from feature_engine.module.clip import Clip
from feature_engine.module.reshape import Reshape
from feature_engine.module.nan_to_num import NanToNum
from feature_engine.module.discret import Discret

operation_dic = {
    "clip":Clip,
    "reshape":Reshape,
    "nan_to_num":NanToNum,
    "discret":Discret
}


class BaseFeatureEngine(object):
    def __init__(self,cfg):
        self.cfg = cfg
        self.operation_dic = operation_dic
        self.operation = self.initOperation(cfg)
    
    def initOperation(self,cfg):
        pass

    def run(self,info_dic):
        for op in self.operation:
            info_dic = op.run(info_dic)
        
        return self.post_process(info_dic)