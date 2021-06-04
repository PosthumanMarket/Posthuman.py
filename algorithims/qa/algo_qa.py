import subprocess
import sys
import json
import os

from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline
from utils import get_job_details
import torch

import subprocess
import sys

i=0

def install():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "transformers"])
    #subprocess.check_call([sys.executable, "-m", "pip", "install", "torch torchvision"])
    i=2

if i==2:
  pass

else:
  install()

import zipfile
job_details = get_job_details()

print('Starting compute job with the following input information:')
print(json.dumps(job_details, sort_keys=True, indent=4))

first_did = job_details['dids'][0]
filename = job_details['files'][first_did][0]
path_to_zip_file = filename
with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
    zip_ref.extractall("/data/outputs")

text = r"""
Bitcoins are created as a reward for a process known as mining.
They can be exchanged for other currencies, products, and services,[10] but the real-world value of the coins is extremely volatile.[11] R
esearch produced by the University of Cambridge estimated that in 2017, there were 2.9 to 5.8 million unique users using a cryptocurrency wallet, most of them using bitcoin.[12]
Users choose to participate in the digital currency for a number of reasons: ideologies such as commitment to anarchism, decentralization and libertarianism, convenience,
using the currency as an investment and pseudonymity of transactions.
"""

q1 = "How many users had bitcoin wallets in 2017?"

generator = pipeline('question-answering', model='/data/outputs/tinybert3a')
#set_seed(42)

answers = generator(question=q1, context=text)
print(answers)
