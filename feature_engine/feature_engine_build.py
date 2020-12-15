from feature_engine.lgb_feature_engine import LgbFeatureEngine
from feature_engine.bert_feature_engine import BertFeatureEngine


feature_engine_dict = {
    "lgb":LgbFeatureEngine,
    "bert":BertFeatureEngine
}

def build_feature_engine(model ,cfg):
    return feature_engine_dict[model](cfg)