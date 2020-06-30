class Model(object):
    def __init__(self,model_cfg,*args, **kwargs):
        super(Model, self).__init__(*args, **kwargs)
        pass

    def build_model(self,input_dim):
        return None

    def dump(self, lossFuncName=None,
            optimizerName=None, basedir=None):
        return None

    def fit(self, X, y, *args, **kwargs):
        
        return None
    
    def predict(self, X_test):
        return None
    
    def summary(self):
        return 'MyModel summary'

    @classmethod
    def restore_model_from_file(cls,mFilename=None):
        
        return mymodel