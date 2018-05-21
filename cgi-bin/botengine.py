from bs4 import BeautifulSoup
from konlpy.tag import Twitter
import os, json, re,random
import requests 
dic_file = "chat-data.json"
twitter = Twitter()
dic ={}
session = requests.session()

def register_dic(words):
    threeDic = ["@"]
    global dic
    if len(words) == 0:return
    for word in words:
        threeDic.append(word[0])
        if len(threeDic) > 3: threeDic = threeDic[1:]
        if len(threeDic) < 3 : continue
        set_words_dic(threeDic,dic)    
        if word[0] == "." or word[0] == "?":
            threeDic = ["@"]
            continue
    json.dump(dic,open(dic_file,'w',encoding='utf-8'))

def set_words_dic(threeWords, dic ):
    s1, s2, s3 = threeWords
    if s1 not in dic:
        dic[s1] = {}
    if s2 not in dic[s1]:
        dic[s1][s2] = {}
    if s3 not in dic[s1][s2]:
        dic[s1][s2][s3] = 0
    dic[s1][s2][s3] +=1


def make_sentence(head):
    if head not in dic:return ""
    ret = []
    if head != "@":ret.append(head)
    top = dic[head]
    w1 = word_choice(top)
    w2 = word_choice(top[w1])
    ret.append(w1)
    ret.append(w2)
    while True:
        if w1 in dic and w2 in dic[w1]:
            w3 = word_choice(dic[w1][w2])
        else: 
            w3 = ""
        ret.append(w3)
        if w3 == "." or w3 =="?" or w3 == "" : break
        w1, w2 = w2, w3
    ret = "".join(ret)
    return grammarCheck(ret)
def word_choice(head):
    li = head.keys()
    return random.choice(list(li))

def grammarCheck(text):
    header = {
            "accept":"*/*",
            "accept-Language":"ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            "accept-encoding":"gzip, deflate, br",
            "referer":"https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EB%84%A4%EC%9D%B4%EB%B2%84+%EB%A7%9E%EC%B6%A4%EB%B2%95+%EA%B2%80%EC%82%AC%EA%B8%B0&oquery=%EB%A7%9E%EC%B6%A4%EB%B2%95+%EA%B2%80%EC%82%AC%EA%B8%B0&tqi=TYFkplpySD0ssbj%2FyLossssstIh-432793"
                ,"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
    }
    url = "https://m.search.naver.com/p/csearch/ocontent/spellchecker.nhn"
    params = {"_callback":"window.__jindo2_callback._spellingCheck_0","q":text}
    res = requests.get(url,params=params,headers=header)
    textLength = len(res.text)
    jsonData = res.text[42:textLength-2]
    jsonData =json.loads(jsonData)
    bsData = BeautifulSoup(jsonData["message"]["result"]["html"],'html.parser')
    return bsData.getText()

def make_reply(text):
    if not text[-1] in [".","?"]: text += "."
    words = twitter.pos(text)
    register_dic(words)
    for word in words:
        face = word[0]
        if face in dic: 
            return make_sentence(face)
    return make_sentence("@")

if os.path.exists(dic_file) :
    dic = json.load(open(dic_file,'r',encoding="utf-8"))
