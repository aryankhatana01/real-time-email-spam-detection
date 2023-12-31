import pandas as pd
import numpy as np
import torch
from sklearn import model_selection
import torch.optim as optim
from torch.utils.data import DataLoader
from transformers import get_linear_schedule_with_warmup
import torch.nn as nn
import warnings

import config
from dataset import EmailDataset
from model import SpamClassifier
from train_fn import train
from eval_fn import evaluate_model

warnings.filterwarnings("ignore")

df = pd.read_csv("../data/processed_data.csv")

df_train, df_val = model_selection.train_test_split(
    df,
    test_size=0.2,
    random_state=42
)

train_ds = EmailDataset(
    spam=df_train['label_num'].to_numpy(),
    msgs=df_train['text'].to_numpy(),
    tokenizer=config.tokenizer,
    max_len=config.MAX_LEN
)

val_ds = EmailDataset(
    spam=df_val['label_num'].to_numpy(),
    msgs=df_val['text'].to_numpy(),
    tokenizer=config.tokenizer,
    max_len=config.MAX_LEN
)

train_dl = DataLoader(
    train_ds,
    batch_size=config.BATCH_SIZE,
    num_workers=4,
    shuffle=True
)

val_dl = DataLoader(
    val_ds,
    batch_size=config.BATCH_SIZE,
    num_workers=4
)

model = SpamClassifier(n_classes=2)
model = model.to(config.device)

optimizer = optim.Adam(model.parameters(), lr=3e-5)

total_steps = len(train_dl) * config.EPOCHS
scheduler = get_linear_schedule_with_warmup(
  optimizer,
  num_warmup_steps=0,
  num_training_steps=total_steps
)

loss_fn = nn.CrossEntropyLoss().to(config.device)

if __name__ == "__main__":
    best_accuracy = 0
    print(f"TRAINING ON {config.device}")
    print("-----------------------------------")
    print()
    for epoch in range(config.EPOCHS):
        print(f'Epoch {epoch + 1}/{config.EPOCHS}')
        print('-' * 10)

        train_acc, train_loss = train(
            model,
            loss_fn,
            optimizer,
            scheduler,
            config.device,
            train_dl,
            len(df_train)
        )

        print(f'Train loss {train_loss} accuracy {train_acc}')

        val_acc, val_loss = evaluate_model(
            model,
            loss_fn,
            config.device,
            val_dl,
            len(df_val)
        )

        print(f'Validation loss {val_loss} accuracy {val_acc}')
        print()

        if val_acc > best_accuracy:
            torch.save(model.state_dict(), 'best_model_state.bin')
            best_accuracy = val_acc
