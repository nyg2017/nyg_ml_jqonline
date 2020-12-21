import numpy as np
import pandas as pd



class BaseModule(object):
    def __init__(self,cfg):
        self.cfg = cfg

    def run(self,info_dict):
        pass

    def run_test(self,info_dict):
        pass



