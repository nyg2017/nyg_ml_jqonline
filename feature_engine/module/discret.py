from feature_engine.module.base_module import BaseModule


class Discret(BaseModule):
    def __init__(self, cfg):  # 可调用name属性
        # super(Class, self).method()
        super(Discret, self).__init__(cfg)

        
    def run(self,info_dict):
        return info_dict
    
    def run_test(self,info_dict):
        return info_dict