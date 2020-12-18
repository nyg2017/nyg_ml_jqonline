from feature_engine.module.base_module import BaseModule
import numpy as np

class NanToNum(BaseModule):

    def __init__(self, cfg):  # 可调用name属性
        # super(Class, self).method()
        super(NanToNum, self).__init__(cfg)


    def run(self,info_dict):
        info_dict["feature"][np.isnan(info_dict["feature"])] = self.cfg["x_fill_value"]
        if not (info_dict["label"] is None):
            info_dict["label"][np.isnan(info_dict["label"])] = self.cfg["y_fill_value"]
        return info_dict