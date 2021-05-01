import subprocess
import sys

i=0
def install():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "transformers"])
    i=2

if i==2:
  pass

else:
  install()

import json
from pathlib import Path
import os
import logging
import pandas as pd
import torch
from transformers import Trainer



from transformers import GPT2Tokenizer, GPT2LMHeadModel
from nltk.tokenize import sent_tokenize
from numpy.random import choice
import torch

# %% Paths to datasets : can be filepath or links. Note: if links are used, filenames are still required for train & eval data.
eval_dataset = Path(os.environ.get("EVAL_DATA", ""))
eval_link = os.environ.get("EVAL_LINK", "") #only needed if eval_data not present locally. Wikitext is available locally
path_logs = Path(os.environ.get("LOGS", "./data/logs"))
dids = json.loads(os.environ.get("DIDS", '[]'))
assert dids, f'no DIDS are defined, cannot continue with the algorithm'
assert eval_dataset, f'no evaluation dataset file defined, cannot continue'

#Download if links

if eval_link:
    os.system('wget '+eval_link)


# Evaluate model performance on a custom dataset : Must be in plaintext format

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

training_args = TrainingArguments(
    output_dir='./results',          # output directory
    num_train_epochs=3,              # total # of training epochs
    per_device_train_batch_size=16,  # batch size per device during training
    per_device_eval_batch_size=64,   # batch size for evaluation
    warmup_steps=500,                # number of warmup steps for learning rate scheduler
    weight_decay=0.01,               # strength of weight decay
    logging_dir='./logs',            # directory for storing logs
)

trainer = Trainer(model=model, args=training_args, tokenizer=tokenizer, eval_dataset=eval_dataset)
trainer.evaluate()
