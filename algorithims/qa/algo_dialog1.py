import subprocess
import sys
import json
import os

import os
import json
import sys

# For use with Posthuman dialog gpt-2 model. Allows conversation -> response interaction with the pretrained AI model.
# edit the "input_text" varible below and publish your own algorithim to test it.

input_text:"How is the weather in china today?"

def get_job_details():
    """Reads in metadata information about assets used by the algo"""
    job = dict()
    job['dids'] = json.loads(os.getenv('DIDS', None))
    job['metadata'] = dict()
    job['files'] = dict()
    job['algo'] = dict()
    job['secret'] = os.getenv('secret', None)
    algo_did = os.getenv('TRANSFORMATION_DID', None)
    if job['dids'] is not None:
        for did in job['dids']:
            # get the ddo from disk
            filename = '/data/ddos/' + did
            print(f'Reading json from {filename}')
            with open(filename) as json_file:
                ddo = json.load(json_file)
                # search for metadata service
                for service in ddo['service']:
                    if service['type'] == 'metadata':
                        job['files'][did] = list()
                        index = 0
                        for file in service['attributes']['main']['files']:
                            job['files'][did].append(
                                '/data/inputs/' + did + '/' + str(index))
                            index = index + 1
    if algo_did is not None:
        job['algo']['did'] = algo_did
        job['algo']['ddo_path'] = '/data/ddos/' + algo_did
    return job

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

from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline
import zipfile
job_details = get_job_details()

print('Starting compute job with the following input information:')
print(json.dumps(job_details, sort_keys=True, indent=4))

first_did = job_details['dids'][0]
filename = job_details['files'][first_did][0]
path_to_zip_file = filename
with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
    zip_ref.extractall("/data/outputs")



# q1 = "How many users had bitcoin wallets in 2017?"


from transformers import AutoTokenizer, AutoModelWithLMHead

tokenizer = AutoTokenizer.from_pretrained("/data/outputs/convgpt")

model = AutoModelWithLMHead.from_pretrained("/data/outputs/convgpt")


user_input_ids = tokenizer.encode(input_text + tokenizer.eos_token, return_tensors='pt')

    # append the new user input tokens to the chat history
    #bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids

    # generated a response while limiting the total chat history to 1000 tokens,
chat_history_ids = model.generate(user_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

    # pretty print last ouput tokens from bot
print("DialoGPT: {}".format(tokenizer.decode(chat_history_ids[:, user_input_ids.shape[-1]:][0], skip_special_tokens=True)))
#print(Response)
