import os
import json
import requests

dirpath = os.path.abspath(os.path.dirname(__file__))
subjectCodeUrl = "https://www.shanghairanking.cn/api/pub/v1/gras/subj?year=2022"
url='https://www.shanghairanking.cn/api/pub/v1/gras/rank?year=2022&subj_code={}'

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
with open(dirpath + "/gras.json", "w", encoding = 'utf-8') as f:
    dict = []
    for subject in subjectCodeset:
        for item in subject["subjs"]:
            dataset = get_url(url.format(item["code"]))['data']['rankings']
            idx = len(dataset)
            for i in range(idx):
                Rank2022 = dataset[i]['ranking']
                univNameCn = dataset[i]['univNameCn']
                region = dataset[i]['region']
                score = dataset[i]['score']
                Q1 = dataset[i]['indData']['26']
                CNCI = dataset[i]['indData']['27']
                IC = dataset[i]['indData']['28']
                TOP = dataset[i]['indData']['29']
                AWARD = dataset[i]['indData']['30']
                dict.append({
                            "领域": subject["nameCn"],
                            "学科": item["nameCn"],
                            "排名": Rank2022,
                            "学校": univNameCn,
                            "国家地区": region,
                            "总分": score,
                            "重要期刊论文数": Q1,
                            "论文标准化影响力": CNCI,
                            "国际合作论文比例": IC,
                            "顶尖期刊论文数": TOP,
                            "教师获权威奖项数": AWARD
                            })
    json.dump(dict, f, ensure_ascii=False, indent=4)
    f.close()