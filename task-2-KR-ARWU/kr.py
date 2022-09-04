import json
import requests
import pandas as pd

df = pd.read_excel("task-2-KR-ARWU/2022软科世界大学学术排名.xlsx", usecols=[4], names=None)  # 读取项目名称列,不要列名
df_li = df.values.tolist()
printf(df_li[0])
printf(df_li[1])
exit(0)
url='https://www.shanghairanking.com/api/pub/v1/arwu/rank?version=2022'

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

dataset = get_url(url)['data']['rankings']
idx = len(dataset)
with open("task-2-KR-ARWU\kr.json", "w", encoding = 'utf-8') as f:
    dict = []
    for i in range(idx):
        WorldRank = dataset[i]['ranking']
        UniName = dataset[i]['univNameEn']
        Region = dataset[i]['region']
        Alumini = dataset[i]['indData']['147']
        Award = dataset[i]['indData']['148']
        HiCi = dataset[i]['indData']['149']
        NS = dataset[i]['indData']['150']
        PCP = dataset[i]['indData']['152']
        PUB = dataset[i]['indData']['151']
        Total = dataset[i]['score']
        dict.append({"排名": WorldRank,
                "学校名称": UniName,
                "国家/地区": Region,
                "总分": Total,
                "校友获奖": Alumini,
                "教师获奖": Award,
                "高被引科学家": HiCi,
                "N&S论文": NS,
                "国际论文": PCP,
                "师均表现": PUB})
    json.dump(dict, f, ensure_ascii=False, indent=4)
    f.close()