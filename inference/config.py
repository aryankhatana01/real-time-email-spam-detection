import torch
from transformers import BertTokenizer

PRE_TRAINED_MODEL_NAME = 'bert-base-cased'
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
tokenizer = BertTokenizer.from_pretrained(PRE_TRAINED_MODEL_NAME)
EPOCHS = 10
MAX_LEN = 512
BATCH_SIZE = 64
MODEL_PATH = "../best_model_state.bin"