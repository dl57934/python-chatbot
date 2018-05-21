import requests
import json
from bs4 import BeautifulSoup
session = requests.session()
url = "https://m.search.naver.com/p/csearch/ocontent/spellchecker.nhn"

header = {
        "accept":"*/*",
        "accept-Language":"ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "accept-encoding":"gzip, deflate, br",
        "referer":"https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EB%84%A4%EC%9D%B4%EB%B2%84+%EB%A7%9E%EC%B6%A4%EB%B2%95+%EA%B2%80%EC%82%AC%EA%B8%B0&oquery=%EB%A7%9E%EC%B6%A4%EB%B2%95+%EA%B2%80%EC%82%AC%EA%B8%B0&tqi=TYFkplpySD0ssbj%2FyLossssstIh-432793"
            ,"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
    }

params = {"_callback":"window.__jindo2_callback._spellingCheck_0","q":"난 너가 제일 싫어"}
res = requests.get(url,params=params,headers=header)
textLength = len(res.text)
jsonData = res.text[42:textLength-2]
jsonData =json.loads(jsonData)
bsData = BeautifulSoup(jsonData["message"]["result"]["html"],'html.parser')
print(bsData.getText())
    
