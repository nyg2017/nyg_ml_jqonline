import sys
if __name__ == "__main__":
    sys.path.append("../nyg_ml_jqonline")

from model.model_base import Model
from sklearn.model_selection import train_test_split
import pickle
import numpy as np 
import json
import lightgbm as lgb


class LGBModel(Model):
    def __init__(self,model_cfg):
        super(LGBModel, self).__init__(model_cfg)
        with open(model_cfg,'r') as f:
            params=json.load(f)
            print (params)
        self.build_params=params['build']
        self.train_params=params['train']
        self.dump_params= params['dump']
        self.predict_params = params['predict']
    
    def build_model(self,input_dim=0):
        train_params=self.build_params

        self.model = lgb.LGBMRegressor(boosting_type=train_params['boosting_type'],
                                       num_leaves=train_params['num_leaves'],
                                       max_depth= train_params['max_depth'],
                                       learning_rate=train_params['learning_rate'],
                                       n_estimators=train_params['n_estimators'],
                                       subsample_for_bin=train_params['subsample_for_bin'],
                                       min_split_gain=train_params['min_split_gain'],
                                       min_child_weight=train_params['min_child_weight'],
                                       min_child_samples=train_params['min_child_samples'],
                                       subsample=train_params['subsample'],
                                       subsample_freq=train_params['subsample_freq'],
                                       colsample_bytree=train_params['colsample_bytree'],
                                       reg_alpha=train_params['reg_alpha'],
                                       reg_lambda=train_params['reg_lambda'],
                                       random_state=3,
                                       n_jobs=train_params['n_jobs'],
                                       silent=train_params['silent'],
                                       importance_type=train_params['importance_type'],
                                       **train_params['other_par'])
    
    def dump(self, lossFuncName=None,optimizerName=None, basedir=None):
        with open(self.dump_params['dump_dir'], 'wb') as fw:
            pickle.dump(self.model, fw)

    def fit(self, X, y, *args, **kwargs):
        y = y.reshape(-1)
        train_params=self.train_params
        X_train, X_test,y_train, y_test = train_test_split(X, y, test_size=train_params['test_size'])
        self.model.fit(X_train,y_train,eval_set=[(X_test,y_test)],eval_metric=train_params['eval_metric'],
                       early_stopping_rounds=train_params['early_stopping_rounds'])

    def predict(self, X_test):
        train_params=self.build_params
        pred_leaf = self.predict_params['pred_leaf']
        #print (pred_leaf)
        #pred_leaf = False
        return self.model.predict(X_test,pred_leaf=pred_leaf,**train_params['other_par'])

    @classmethod
    def restore_model_from_file(cls,model_cfg):
        mymodel=LGBModel(model_cfg)
        m_file = mymodel.dump_params['dump_dir']
        with open(m_file, 'rb') as fr:
            model = pickle.load(fr)
        mymodel.model=model
        return mymodel

if __name__ == "__main__":
    #sys.path.append('../..')
    model_cfg = './config/light_config.json'
    M=LGBModel(model_cfg)
    M.build_model()
    x=np.random.rand(10000,10)
    y=np.random.rand(10000)
    M.fit(x,y)
    print(M.predict(x)[1])
    print (len(M.model.booster_.dump_model()["tree_info"]),M.model.num_leaves)
    M.dump()
    M = LGBModel.restore_model_from_file(model_cfg,"./model_saved/lightgbm.txt")
    print (M.predict(x))