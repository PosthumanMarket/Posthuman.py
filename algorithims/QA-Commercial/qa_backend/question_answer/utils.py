
import sys
sys.path.append('/home/ubuntu/drqa_nlp2')
sys.path.append('/home/ubuntu')
from drqa_nlp2.scripts.retriever import interactive
#from drx.drqa_nlp2.scripts.retriever import interactivex
#from drw.drqa_nlp2.scripts.retriever import interactivew
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktTrainer
#from bert_serving.client import BertClient
import tensorflow as tf
import numpy as np
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline
import zipfile

generator = pipeline('question-answering', model='/data/outputs/tinybert3a')
#set_seed(42)


#sys.path.append("/home/khetz96/pytorch-pretrained-BERT")
#from pytorch_pretrained_bert import BertConfig, BertForTokenClassification, load_tf_weights_in_bert, BertForQuestionAnswering
#config = BertConfig.from_json_file('/home/khetz96/pytorch-pretrained-BERT/wwm_uncased_L-24_H-1024_A-16/bert_config.json')
#model = BertForQuestionAnswering(config)
#device = torch.device("cuda")
#torch.device("cuda" if torch.cuda.is_available() else "cpu")
#model.load_state_dict(torch.load(init_checkpoint, map_location='cuda:0'))
#model.to(device)
import os

#sys.path.append("/home/khetz96/pyt-bert/pytorch_pretrained_bert")
#from BERT10 import main1
os.chdir("/home/ubuntu/qa.luci.ai")


trainer = PunktTrainer()
trainer.INCLUDE_ALL_COLLOCS = True

tokenizer2 = PunktSentenceTokenizer(trainer.get_params())

tokenizer2._params.abbrev_types.add("art")
tokenizer2._params.abbrev_types.add("s")
tokenizer2._params.abbrev_types.add("c")
tokenizer2._params.abbrev_types.add("h")
tokenizer2._params.abbrev_types.add("c")
tokenizer2._params.abbrev_types.add("anr")
tokenizer2._params.abbrev_types.add("ors")
tokenizer2._params.abbrev_types.add("ss")
tokenizer2._params.abbrev_types.add("reg")
tokenizer2._params.abbrev_types.add("a")
tokenizer2._params.abbrev_types.add("i")
tokenizer2._params.abbrev_types.add("r")
tokenizer2._params.abbrev_types.add("v")
tokenizer2._params.abbrev_types.add("vs")
tokenizer2._params.abbrev_types.add("j")
tokenizer2._params.abbrev_types.add("l")
tokenizer2._params.abbrev_types.add("p")
tokenizer2._params.abbrev_types.add("arts")
tokenizer2._params.abbrev_types.add("dr")
tokenizer2._params.abbrev_types.add("cls")

#bert_client = BertClient(ip="34.80.146.187", port=5545, port_out=5546)


def _decode_record(record):
    # NOTE: Check if needed
    """Decodes a record to a TensorFlow example."""
    return tf.parse_single_example(
        record,
        {
            "features": tf.FixedLenFeature([768], tf.float32),
            "labels": tf.FixedLenFeature([], tf.int64),
        },
    )




#tokenizer = AutoTokenizer.from_pretrained("google/electra-base-discriminator")
#model = AutoModelForQuestionAnswering.from_pretrained("checkpoint-2500")

def find_ans(questions, text):
  for question in questions:
    #with torch.cuda.device(0):
        inputs = tokenizer.encode_plus(question, text, add_special_tokens=True, return_tensors="pt")
        #inputs = inputs.cuda(async=True)
        input_ids = inputs["input_ids"].tolist()[0]
        text_tokens = tokenizer.convert_ids_to_tokens(input_ids)
        answer_start_scores, answer_end_scores = model(**inputs)
        print(answer_start_scores, answer_end_scores)
        answer_start = torch.argmax(
            answer_start_scores
        )  # Get the most likely beginning of answer with the argmax of the score
        answer_end = torch.argmax(answer_end_scores) + 1  # Get the most likely end of answer with the argmax of the score
        answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))
        print(f"Question: {question}")
        print(f"Answer: {answer}\n")
        adict={}
        adict['ans']=answer
        adict['probability']=answer_end_scores
        adict['text']=text
        return adict



"""def sort_sent_pair_embeds(sent_pair_embeds, sentences, threshold=0.3):
    i=0
    eo=[]
    eo_cont=[]
    eid=[]
    eprob=[]
    if plist=="True":
        for ent in sent_pair_embeds:
            i += 1
            print(ent)
            if float(ent[0]) > threshold:
                    try:
                        ans=sentences[i]
                        for para in xlist:
                            if ans in para['text']:
                                cont=str(para['text'])+str(para['id'][0:150])
                                eid.append(para['id'][0:150])
                                eo_cont.append([cont])
                                eo.append(ans)
                        eprob.append(ent[0])
                    except:
                        continue


    if sentences!=[] and plist=="False":
        for ent in sent_pair_embeds:
            i += 1
            print(ent)
            if float(ent[0]) > threshold:
                try:
                    eo.append(sentences[i-1])
                    eo_cont.append(sentences[i-3 : i+3])
                except:
                    eo.append(sentences[i])
                    eo_cont.append(sentences[i-1 : i+1])
                if eo_cont == "":
                    eo_cont.append(sentences[i - 1 : i + 1])
                eprob.append(ent[0])

    if sentences==[] and plist=="False":
        for ent in sent_pair_embeds:
                i += 1
                print(ent)
                if float(ent[0]) > threshold:
                    try:
                        eo.append(xlist[i-1]['sentence'])
                        eo_cont.append(xlist[i-1]['context'])
                    except:
                        eo.append(xlist[i]['sentence'])
                        eo_cont.append(xlist[i]['context'])
                    if eo_cont == "":
                        eo_cont.append(sentences[i - 1 : i + 1])
                    eprob.append(ent[0])
    i = -1
    alist = []
    for ans in eo:
        i += 1
        adict = {}
        adict["sentence"] = ans
        adict["context"] = eo_cont[i]
        adict["probability"] = eprob[i]
        adict["id"] = eid[i]
        alist.append(adict.copy())
        # a_list=[]
        # sort alist by probabilities
    topk = 20
    sorted_answers = sorted(alist, key=lambda item: item["probability"], reverse=True)
    sa=[]
    for a in sorted_answers:
        #sa.append(" ".join(sent for sent in a["context"]))
        sa.append(a["sentence"])
    alist2 = []
    ape = ""
    for a2 in sorted_answers:
        i += 1
        adict2 = {}
        if a2["sentence"] != ape:
            if len(a2["sentence"]) > 30:
                adict2["sentence"] = a2["sentence"]
                adict2["context"] = a2["context"]
                adict2["probability"] = str(a2["probability"])
                adict2["id"] = a2['id']
                alist2.append(adict2.copy())
        ape = a2["sentence"]
    return alist2"""

def a2(list):
    # query_vec = bc.encode([query2])[0]
    # i+=1
    topk = 20
    # score = np.sum(query_vec * doc_vecs, axis=1) / np.linalg.norm(doc_vecs, axis=1)
    topk_idx = np.argsort(list)[::-1][:topk]
    # allr.append(s2.copy)
    # q3=qx
    # print('top %d questions similar to "%s"' % (topk, colored(query, 'green')))
    a_list = []
    """for idx in topk_idx:
        #print('> %s\t%s' % (colored('%.1f' % score[idx], 'cyan'), colored(sent_pairs[idx], 'yellow')))
        #a_list.append(devdat[idx])
        s2={}
        s2["score"]=score[idx]
        s2["sent"]=sent2[idx]
        a_list.append(s2.copy())
    return a_list"""
"""def char_ans(contexts, question):
    Ans= main1(model,bert_config_file="/home/khetz96/bert-as-service/bert-as-service/wwm_uncased_L-24_H-1024_A-16/bert_config.json", predict_file=contexts, question1=question, n_best_size=10, vocab_file="/home/khetz96/bert-as-service/bert-as-service/wwm_uncased_L-24_H-1024_A-16/vocab.txt")
    print("axeeee")
    print(Ans)
    return Ans"""

def top_n_paras(query, n=10):
    ptext = interactive.process(query, k=25)
    #ptext1= interactivew.processw(query, k=n)
    #ptext2= interactivex.processx(query, k=25)
    #ptext3= ptext2+ptext
    return [{"text": ptext}]
