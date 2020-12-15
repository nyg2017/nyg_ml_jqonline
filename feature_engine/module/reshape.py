from feature_engine.module.base_module import BaseModule


class Reshape(BaseModule):

    def __init__(self, cfg):  # 可调用name属性
        # super(Class, self).method()
        super(Reshape, self).__init__(cfg)


    def run(self,feature,label):
        return feature,label