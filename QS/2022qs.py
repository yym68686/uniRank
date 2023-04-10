import re
import json
import requests

urlen = "https://www.topuniversities.com/sites/default/files/qs-rankings-data/en/3816281_indicators.txt?rdeqg3"
urlcn = "https://www.qschina.cn/sites/default/files/qs-rankings-data/cn/2174878_indicators.txt"
eo = {urlen: "ind_3819456", urlcn: "ind_2177844"}
url = urlcn
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
}

# 获取数据
def get_page(url):
    try:
        r = requests.get(url, headers=headers)
        # print(r.text[:1000])
        if r.status_code == 200:
            return r.json()
    except requests.ConnectionError as e:
        print(e)

# 解析数据
def parser_page(json):
    if json:
        items = json.get('data')
        for i in range(len(items)):
            item = items[i]
            qsrank = {}
            if "=" in item['overall_rank_dis']:
                rk_str = str(item['overall_rank_dis']).split('=')[-1]
                qsrank['overall_rank_dis'] = rk_str
            else:
                qsrank['overall_rank_dis'] = item['overall_rank_dis']
            qsrank['uni'] = item['uni']
            qsrank['region'] = item['location']
            qsrank['overall'] = item['overall']
            qsrank['International Students Ratio'] = item['ind_14']
            qsrank['International Research Network'] = item['ind_15']
            qsrank['International Faculty Ratio'] = item['ind_18']
            qsrank['Faculty Student Ratio'] = item['ind_36']
            qsrank['Citations per Faculty'] = item['ind_73']
            qsrank['Academic Reputation'] = item['ind_76']
            qsrank['Employer Reputation'] = item['ind_77']
            qsrank['Employment Outcomes'] = item[eo[url]]
            yield qsrank

# 主函数
def main():
    json1 = get_page(url)
    results = parser_page(json1)
    with open("qscn.json", "w", encoding = 'utf-8') as f: # path 是文件要存储的地方
        dict = []
        for result in results:
            rankresult = re.findall("\"td-wrap-in\">(.*?)</div>|(.*?)</div>", result['overall_rank_dis'])
            if rankresult[0][0] != "":
                rank = rankresult[0][0]
            else:
                rank = rankresult[0][1]
            nameresult = re.findall("class=\"uni-link\">(.*?)</a>", result['uni'])
            scoreresult = re.findall("\"td-wrap-in\">(.*?)</div>", result['overall'])
            isr = re.findall("\"td-wrap-in\">(.*?)</div>", result['International Students Ratio'])
            irn = re.findall("\"td-wrap-in\">(.*?)</div>", result['International Research Network'])
            ifr = re.findall("\"td-wrap-in\">(.*?)</div>", result['International Faculty Ratio'])
            fsr = re.findall("\"td-wrap-in\">(.*?)</div>", result['Faculty Student Ratio'])
            cpf = re.findall("\"td-wrap-in\">(.*?)</div>", result['Citations per Faculty'])
            ar = re.findall("\"td-wrap-in\">(.*?)</div>", result['Academic Reputation'])
            er = re.findall("\"td-wrap-in\">(.*?)</div>", result['Employer Reputation'])
            eo = re.findall("\"td-wrap-in\">(.*?)</div>", result['Employment Outcomes'])
            # dict.append({"rank": rank,
            #              "name": nameresult[0],
            #              "region": result['region'],
            #              "score": scoreresult[0],
            #              "Academic Reputation": ar[0],
            #              "Employer Reputation": er[0],
            #              "Citations per Faculty": cpf[0],
            #              "Faculty Student Ratio": fsr[0],
            #              "International Students Ratio": isr[0],
            #              "International Faculty Ratio": ifr[0],
            #              "International Research Network": irn[0],
            #              "Employment Outcomes": eo[0]})
            dict.append({"排名": rank,
                         "大学": nameresult[0],
                         "地区": result['region'],
                         "综合得分": scoreresult[0],
                         "学术声誉": ar[0],
                         "雇主声誉": er[0],
                         "每位教员引用率": cpf[0],
                         "师生比": fsr[0],
                         "国际学生比例": isr[0],
                         "国际教师比例": ifr[0],
                         "国际研究网络": irn[0],
                         "就业结果": eo[0]})
        json.dump(dict, f, ensure_ascii=False, indent=4)
        f.close()

main()

