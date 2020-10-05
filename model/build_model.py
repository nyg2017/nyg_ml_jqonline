from model.lgb import LGBModel
import json



model_dict = {
    "lgb":LGBModel
}

def build_model(model_name,model_cfg):
    #with open(model_cfg,"r") as f:
    #    model_cfg = json.load(f)
    model = model_dict[model_name](model_cfg)
    model.build_model()
    return model

def restore_model_from_file(model_name,model_cfg):
    model = model_dict[model_name].restore_model_from_file(model_cfg)
    return model
