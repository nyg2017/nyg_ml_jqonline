import numpy as np
import pandas as pd



class BaseModule(object):
    def __init__(self,cfg):
        self.cfg = cfg

    def run(self,feature,label):
        pass



