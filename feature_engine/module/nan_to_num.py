from feature_engine.module.base_module import BaseModule


class NanToNum(BaseModule):

    def __init__(self, cfg):  # 可调用name属性
        # super(Class, self).method()
        super(NanToNum, self).__init__(cfg)


    def run(self,feature,label):
        return feature,label