from feature_engine.module.base_module import BaseModule
import numpy as np

class Clip(BaseModule):
    def __init__(self, cfg):  # 可调用name属性
        # super(Class, self).method()
        super(Clip, self).__init__(cfg)

    def run(self,info_dict):
        if not (info_dict["label"] is None):
            label = np.abs(info_dict["label"])
            clip_value = self.cfg["clip_value"]
            index = label < clip_value

            info_dict["label_clip_index"] = index

        return info_dict
    
    def run_test(self,info_dict):
        return info_dict