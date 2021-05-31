import subprocess
import sys


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






i=0
def install():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "transformers"])
    i=2

if i==2:
  pass

else:
  install()

infer_text="A mummy is a dead human or an animal whose soft tissues and organs have been preserved by either intentional or accidental exposure to chemicals, extreme cold, very low humidity, "

from transformers import pipeline, set_seed
import sys
import os

import zipfile
job_details = get_job_details()

print('Starting compute job with the following input information:')
print(json.dumps(job_details, sort_keys=True, indent=4))

first_did = job_details['dids'][0]
filename = job_details['files'][first_did][0]
path_to_zip_file = filename
with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
    zip_ref.extractall("/data/outputs/distilgpt2")

generator = pipeline('text-generation', model='/data/outputs/distilgpt2')
set_seed(42)


def complete_text(text):
    r = generator(text, max_length=200, num_return_sequences=5)
    return r

def main():
    result = complete_text(infer_text) # generates continuation text starting at infer text. Text continuation can be adapted to all NLP tasks including classification
    print(result)
    r2 = {}
    r2['returned_Text'] = str(result)
    r3 = str(r2)
    return r3

result = complete_text(infer_text) # generates continuation text starting at infer text. Text continuation can be adapted to all NLP tasks including classification
r2 = {}
r2['returned_Text'] = str(result)
r3 = str(r2)
print(r3)
