from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
#from drq.drqa_nlp2.scripts.retriever import interactiveq
from .utils import tokenizer2, top_n_paras, find_ans
#from bert_serving.client import BertClient
import numpy as np
from termcolor import colored
import random
import time
import os
import sys
import re
import sys
sys.path.append('/home/ubuntu/drqa_nlp2')
sys.path.append('/home/ubuntu')


from .models import UserAnswer
topk=500
"""gold1=[]
gold2=[]
gold3=[]
gold1=json.load(open("gold-26k.json"))
gold2=json.load(open("gold-cit15k.json")) 
gold3=json.load(open("gold-cit14k.json"))
gold4=json.load(open("gold170k.json"))
goldx=[]
for x in gold1:
    goldx.append(x)
for x in gold2:
    goldx.append(x)
for x in gold3:
    goldx.append(x)
for x in gold4:
    goldx.append(x)
    
qlist=[]
gold=goldx
for a in gold:
    try:
        q=a['question']
        if q!='':
            qlist.append(q)
        else:
            qlist.append("no q")
    except:
        continue
"""
#bc=BertClient(ip="130.211.213.156", port=5545, port_out=5546, check_version=False)
#doc_vecs=bc.encode(qlist)



from celery import shared_task

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__
topk=50
gold1=[]
gold2=[]
gold4=[]
gold3=[]
#gold1=json.load(open("gold-26k.json"))[:10]
#gold4=json.load(open("gold-34k_a.json"))
#gold2=json.load(open("gold-cit15k.json")) 
#gold3=json.load(open("gold-cit14k.json"))[0:1]
#gold4=json.load(open("gold170k.json"))

goldx=[]
for x in gold1:
    x2=x['sentence']+"ooo"
    d=re.findall("A\:(.+?)ooo", x2)
    if d!=[]:
        e="".join(d)
    else:
        e=x['sentence']
    c={}
    c['sentence']=e
    c['probability']=x['probability']
    c['context']=x['context']
    c['question']=x['question']
    goldx.append(c.copy())
for x in gold2:
    x2=x['sentence']+"ooo"
    d=re.findall("A\:(.+?)ooo", x2)
    if d!=[]:
        e="".join(d)
    else:
        e=x['sentence']
    c={}
    c['sentence']=e
    c['probability']=x['probability']
    c['context']=x['context']
    c['question']=x['question']
    goldx.append(c.copy())
for x in gold3:
    x2=x['sentence']+"ooo"
    d=re.findall("A\:(.+?)ooo", x2)
    if d!=[]:
        e="".join(d)
    else:
        e=x['sentence']
    c={}
    c['sentence']=e
    c['probability']=x['probability']
    c['context']=x['context']
    c['question']=x['question']
    goldx.append(c.copy())
for x in gold4:
    x2=x['sentence']+"ooo"
    d=re.findall("A\:(.+?)ooo", x2)
    if d!=[]:
        e="".join(d)
    else:
        e=x['sentence']
    c={}
    c['sentence']=e
    c['probability']=x['probability']
    c['context']=x['context']
    c['question']=x['question']
    goldx.append(c.copy())
qlist=[]
gold=[]
for a in goldx:
    e={}
    e['question']=a['question']
    e['sentence']=a['sentence']
    e['probability']=a['probability']
    e['context']=[str(a['context'])]
    q=a['question']
    if q!='':
        qlist.append(q)
    else:
        qlist.append("no q")
    gold.append(e)
    



# bc = bert_client(ip="35.184.66.137", port=5555, port_out=5556)
# Test if server is up
def ping(request):
    return HttpResponse("Pong")


def sort_nbest1(nbest, plist2):
    tnbest = str(nbest)
    texts = re.findall("'text'(.+?)\)")


def sort_nbest(nbest, plist2, sentences, threshold=0.01):
  a=[]
  dic=nbest
  for key in dic:
    for x in dic[key]:
      a.append(x)
  #return a
  #s=sorted(a, key=lambda k:k['probability'], reverse=True)
  #s=sorted(a, key=lambda k:(2*k.start_logit+k.end_logit+5k.probability), reverse=True)
  #print(s)
  alist=[]
  kv=[]
  i=0
  im=0
  enablePrint()
  for b in a:
    subk=[]
    for key, value in b.items():
        im+=1
        print("x iter"+str(im))
        k={}
        #k["context"]="china"
        if key=="text":
            if 70 < len(value) < 450:
                k["sentence"]=value
        if key=="probability" or key=="start_logit" or key=="end_logit":
            i+=1
            k[key]=value
            i=0
        subk.append(k.copy())
    kv.append(subk)
  print(kv)
  alist=[]
  apro=0.5
  sent2={}
  sent2["sentence"]="china"
  sent2["sentence2"]="china"
  ix=0
  ixo=0
  enablePrint()
  for list in kv:
        ix+=1
        print("second iter"+str(ix))
        ax={}
        ax["sentence"]="hop"
        ansx=ax["sentence"]
        ax["sentence2"]="no matched sentence"
        for dict in list:
            try:
                ax["sentence"]=dict["sentence"]
                ansx=dict["sentence"]
            except:
                try:
                    ax["start_logit"]=dict["start_logit"]
                    asl=dict["start_logit"]
                except:
                    try:
                        ax["end_logit"]=dict["end_logit"]
                        ael=dict["end_logit"]
                        apro=dict["probability"]
                    except:
                        continue
        ax["probability"]=(asl+ael+4*apro)/18
        ax["context"]=["foo"]
        print(ax)
        if ax["sentence"]!="hop":
            if ax["probability"] > threshold:
                #if sent2["sentence"] in ax["sentence"] or ax["sentence"] in sent2["sentence"]:
                    #continue
                    for para in plist2:
                        if ansx in str(para):
                            p2=para
                            ax["context"]=[str(p2)]
                            ax['id']=p2['id'][0:150]
                    for sentence in sentences:
                        if ansx in sentence:
                            ax["sentence2"]=sentence
                    if ax["context"]==["foo"]:
                        ax['context']=[ax['sentence2']]
                    if ax["sentence2"]==sent2["sentence2"]:
                        ax["sentence"]=ax["sentence2"]
                    if ax["context"]==["foo"]:
                        ax['context']=ax['sentence2']
            alist.append(ax.copy())
            sent2=ax
  return alist

def nbest3(kv):
  alist=[]
  for info in kv:
      a={}
      i2=str(info)
      sent=re.findall('"sentence"\: (.+?)\}', i2)
      sl=re.findall('"start_logit"\: (.+?)\}', i2)
      el=re.findall('"end_logit"\: (.+?)\}', i2)
      sl2="".join(sl)
      el2="".join(el)
      prob=float(sl2)+float(el2)
      a["sentence"]=sent
      a["probability"]=prob
      a["context"]=["chx"]
      alist.append(a.copy())
  print(alist)
  return alist

yes=True
# Response logic for the search endpoint
@csrf_exempt
def search(request):
    query = request.GET.get("query")
    if not query:
        raise Http404("Please request with proper params")
    print("thanks for asking!")
    if yes==True:
        paras = top_n_paras(query, n=20)
        #paras=pars
        p2 = []
        parasx = []
        for para in paras:
            parasx.append(str(para['text']))
        plist = ";".join([str(para["text"]) for para in paras]) # one text in dict
        plist2 = re.findall("'text'\:(.+?)}", plist) # actual text from id-text extracted using regex
        plist_id = re.findall("'id'\:(.+?)}", plist) # actual text from id-text extracted using regex
        plist3 = []
        plist4=[]
        i=-1
        for p in plist2:
            i+=1
            p2=p.replace("YY", "")
            p3={}
            p3["id"]=plist_id[i]
            p3["text"]=p2
            plist3.append(p3)
            plist4.append(p2)
        #plist3 = plist2[0:6] + plist2[12:22]
        plist4=plist4
        plist5=plist3
        pcont = ";".join([str(para) for para in plist4]) # join all "text"
        alist=[]
        for p in plist4:
            Ans=find_ans([query], p)
            alist.append(Ans)
        #clist=sort_nbest(Ans, plist3, sentences)
        #sent_pair_embed = bert_client.fetch_all(concat=True)
        #alist2=sort_sent_pair_embeds(sent_pair_embed, sentences, threshold=0.4)
        alst=[]
        i=0
        """ans2={}
        ans2["sentence"]="china"
        for ans in alist2:
            i+=1
            if i<10:
                if ans["sentence"]!=ans2["sentence"]:
                    atext=" ".join(ans["context"])
                    alst.append(atext)
                    ans2=ans
        astr=" ".join(alst)
        #Ans=char_ans([astr], query)
        #clist=sort_nbest(Ans, plist2, sentences, threshold=0.4)
        #sent_pair_embed = [["0.9", "0.5"]]
        eo = []
        eo_cont = []
        eprob = []
        i = 0
        #gold_par=" ".join(s for s in sa[0:6])
        #print(len(plist2))
        #sorted_clist=sorted(clist, key=lambda item: float(item["probability"]), reverse=True)
        """
        answers={}
        xlist1=[]
        i=-1
        u=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
        for a in u:
            i+=1
            try:
                xlist1.append(alist[i])
            except:
                print("cry")
            try:
                xlist1.append(alist[i])
            except:
                print("bye")


    #sort based on combined probs
    #xlist1=sorted_clist[0:8]

        xlist=sorted(xlist1, key=lambda item: float(item["probability"]), reverse=True)
        answers["answers"] = xlist[0:10]
        print(answers["answers"])
        print(len(plist2))
        probability_threshold = 0.5
        probability_threshold2 = 0.4
        print("documents searched " + "1,209,148")
        print("documents read " + str(num_docs))
        print("sentences read " + str(num_sent))
        print("words read:" + str(num_words))
        import uuid
        pt=str(uuid.uuid4())
        pt2=pt+".json"
        c="ok"
        #print(score)
        with open(pt2, 'w') as writer:
            json.dump(answers, writer)
        if all(float(item["probability"]) < probability_threshold for item in clist):
            if all(float(item["probability"]) < probability_threshold2 for item in alist2):
                return {"success": False}
            else:
                answers["success"] = True
                answers["answers"] = alist2[0:10]
                return answers
        else:
            answers["success"] = True
            return answers

def search_request(request):
    print("godddit")
    query = request.GET.get("query")
    if not query:
        raise Http404("Please request with proper params")
    else:
        result = search.delay(query)
    while not result.ready():
        pass
    task = result.get()
    return JsonResponse(task)
