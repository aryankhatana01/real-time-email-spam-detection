import torch
import config
from test_dataset import TestDataset
from torch.utils.data import DataLoader
from model import SpamClassifier
import numpy as np

def create_dl(msg):
    ds = TestDataset(
        msgs=msg,
    )

    return DataLoader(
        ds,
        batch_size=1,
    )

def inference_fn(
    model,
    msg, 
):
    model = model.eval()
    data_loader = create_dl(msg)

    msgs = []
    predictions = []
    predictions_probs = []

    with torch.inference_mode():
        for d in data_loader:
            msg = d['msg']
            input_ids = d['input_ids'].to(config.device)
            attention_masks = d['attention_mask'].to(config.device)

            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_masks
            )

            _, preds = torch.max(outputs, dim=1)

            probs = torch.nn.functional.softmax(outputs, dim=1)

            msgs.extend(msg)
            predictions.extend(preds)
            predictions_probs.extend(probs)

    predictions = torch.stack(predictions).cpu()
    predictions_probs = torch.stack(predictions_probs).cpu()
    return msgs, predictions, predictions_probs

if __name__ == "__main__":
    model = SpamClassifier(n_classes=2)
    model.load_state_dict(torch.load(config.MODEL_PATH))
    model = model.to(config.device)

    msg = np.array(["Subject: You have won a lottery."])

    msgs, predictions, predictions_probs = inference_fn(
        model=model,
        msg=msg
    )

    print(predictions)
    print(predictions_probs)
    print(msgs)