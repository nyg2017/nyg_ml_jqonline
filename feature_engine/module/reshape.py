from feature_engine.module.base_module import BaseModule


class Reshape(BaseModule):

    def run(self,feature,label):
        return feature,label