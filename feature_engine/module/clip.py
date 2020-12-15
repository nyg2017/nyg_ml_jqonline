from feature_engine.module.base_module import BaseModule


class Clip(BaseModule):

    def run(self,feature,label):
        return feature,label