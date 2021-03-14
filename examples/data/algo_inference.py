from transformers import pipeline, set_seed
import sys
import os

generator = pipeline('text-generation', model='gpt2')
set_seed(42)

#Define inference text to continue in a file. Links also accepted
inference_file = os.environ.get("Inference_text_file", "")
inference_link = os.environ.get("Inference_Link", "")


if inference_link:
    os.system('wget '+inference_link)

#read from inference file

#with open(inference_file) as f:
    #infer_text = f.read()

infer_text = "hello my name is "

def complete_text(text):
    r = generator(text, max_length=60, num_return_sequences=5)
    return r

def main():
    result = complete_text(infer_text) # generates continuation text starting at infer text. Text continuation can be adapted to all NLP tasks including classification
    print(result)
    return(result)

result = complete_text(infer_text) # generates continuation text starting at infer text. Text continuation can be adapted to all NLP tasks including classification
print(result)
return(result)
