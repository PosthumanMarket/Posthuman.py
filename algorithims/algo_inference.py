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

infer_text="A mummy is a dead human or an animal whose soft tissues and organs have been preserved by either intentional or accidental exposure to chemicals, extreme cold, very low humidity, "

from transformers import pipeline, set_seed
import sys
import os

generator = pipeline('text-generation', model='distilgpt2')
set_seed(42)

#Define inference text to continue in a file. Links also accepted
inference_file = os.environ.get("Inference_text_file", "")
inference_link = os.environ.get("Inference_Link", "")


if inference_link:
    os.system('wget '+inference_link)

#read from inference file

#with open(inference_file) as f:
    #infer_text = f.read()

infer_text2 = "hello my name is "

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
