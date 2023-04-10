import os
import json
import requests
# import pandas as pd

dirpath = os.path.abspath(os.path.dirname(__file__))
subjectCodeUrl = "https://www.shanghairanking.cn/api/pub/v1/bcsr/subj?year=2022"
url='https://www.shanghairanking.cn/api/pub/v1/bcsr/rank?target_yr=2022&subj_code={}'

def get_url(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Referer':'https://shanghairanking.com/',
        'DNT':'1',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Connection':'keep-alive',
        'Accept-Language':'zh-CN,zh;q=0.9,en-CN;q=0.8,en;q=0.7',
        'Accept-Encoding':'gzip, deflate',
    }
    req = requests.get(url, headers=headers)
    req.encoding='utf-8'
    html = req.json()
    return html


subjectCodeset = get_url(subjectCodeUrl)['data']
with open(dirpath + "/bcsr.json", "w", encoding = 'utf-8') as f:
    dict = []
    for subject in subjectCodeset:
        for item in subject["subjs"]:
            dataset = get_url(url.format(item["code"]))['data']['rankings']
            idx = len(dataset)
            for i in range(idx):
                Rank2022 = dataset[i]['ranking']
                try:
                    Rank2021 = dataset[i]['contrastRanking']['2021']
                except:
                    Rank2021 = "无"
                rankPctTop = dataset[i]['rankPctTop']
                univNameCn = dataset[i]['univNameCn']
                score = dataset[i]['score']
                dict.append({"2022排名": Rank2022,
                            "2021排名": Rank2021,
                            "全部层次": rankPctTop,
                            "学校": univNameCn,
                            "总分": score,
                            "学科门类": subject["nameCn"],
                            "学科": item["nameCn"]})
    json.dump(dict, f, ensure_ascii=False, indent=4)
    f.close()