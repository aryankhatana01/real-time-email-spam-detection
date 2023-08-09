from inference.model import SpamClassifier
from inference import config as model_cfg
import torch

def get_configured_model():
    model = SpamClassifier(n_classes=2)
    if model_cfg.device == torch.device('cpu'):
        model.load_state_dict(torch.load(model_cfg.MODEL_PATH, map_location=torch.device('cpu')))
    else:
        model.load_state_dict(torch.load(model_cfg.MODEL_PATH))
    model = model.to(model_cfg.device)
    return model