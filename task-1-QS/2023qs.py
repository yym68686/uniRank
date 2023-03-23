import os
import re
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup

baseurl = "https://www.qschina.cn"
urlcn = "https://www.qschina.cn/sites/default/files/qs-rankings-data/cn/{}_indicators.txt"
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
}

def get_subject_data(url, name):
    if os.path.exists(name):
        with open(name, "r", encoding = 'utf-8') as f:
            return json.load(f)
    else:
        try:
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                select = soup.select('.subject-select')
                regex = r"value=\"(.*?)\">\s(.*?)\s<"
                matches = re.finditer(regex, str(select), re.MULTILINE)
                dict = {}
                for match in matches:
                    dict[match.group(1)] = match.group(2)
                with open(name, "w", encoding = 'utf-8') as f:
                    json.dump(dict, f, ensure_ascii=False, indent=4)
                    f.close()
                with open(name, "r", encoding = 'utf-8') as f:
                    return json.load(f)
        except requests.ConnectionError as e:
            print(e)

def get_raw_data(url, subject):
    if os.path.exists(f"{subject}.json"):
        with open(f"{subject}.json", "r", encoding = 'utf-8') as f:
            return json.load(f).get('data')
    else:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            regex = r"node\\/(.*?)\""
            matches = re.findall(regex, r.text, re.MULTILINE)
            pageid = matches[0]
        print(subject, urlcn.format(pageid))
        r = requests.get(urlcn.format(pageid), headers=headers)
        if r.status_code == 200:
            with open(f"{subject}.json", "w", encoding = 'utf-8') as f:
                data = eval(re.sub(r'<.*?>', '', str(r.json())))
                json.dump(data, f, ensure_ascii=False, indent=4)
                f.close()
            with open(f"{subject}.json", "r", encoding = 'utf-8') as f:
                return json.load(f).get('data')

def get_json_data(url, name):
    if os.path.exists(name):
        with open(name, "r", encoding = 'utf-8') as f:
            return json.load(f)
    else:
        try:
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                with open(name, "w", encoding = 'utf-8') as f:
                    json.dump(r.json(), f, ensure_ascii=False, indent=4)
                    f.close()
                with open(name, "r", encoding = 'utf-8') as f:
                    return json.load(f)
        except requests.ConnectionError as e:
            print(e)

def parser_page(items, subject):
    print("=>", subject)
    for i in range(len(items)):
        qsrank = {}
        item = items[i]
        qsrank['学科'] = subject
        qsrank['区域'] = item['region']
        qsrank['地区'] = item['location']
        qsrank['总体排名'] = item['overall_rank']
        qsrank['总体排名(包含并列)'] = item['overall_rank_dis']
        qsrank['大学名称'] = item['uni']
        qsrank['综合得分'] = item['overall']

        qsrank['学术声誉'] = item['ind_76']
        qsrank['学术声誉排名(包含并列)'] = item['rank_d_76']
        qsrank['学术声誉排名'] = item['rank_76']

        qsrank['雇主声誉'] = item['ind_77']
        qsrank['雇主声誉排名(包含并列)'] = item['rank_d_77']
        qsrank['雇主声誉排名'] = item['rank_77']

        qsrank['论文篇均引用率'] = item['ind_70']
        qsrank['论文篇均引用率排名(包含并列)'] = item['rank_d_70']
        qsrank['论文篇均引用率排名'] = item['rank_70']

        qsrank['H指数'] = item['ind_69']
        qsrank['H指数排名排名(包含并列)'] = item['rank_d_69']
        qsrank['H指数排名'] = item['rank_69']

        qsrank['国际研究网络'] = item.get('ind_15', '')
        qsrank['国际研究网络排名(包含并列)'] = item.get('rank_d_15', '')
        qsrank['国际研究网络排名'] = item.get('rank_15', '')
        yield qsrank
        
def main():
    subjecturl = "https://www.qschina.cn/university-rankings/university-subject-rankings/2023/anthropology"
    df = pd.DataFrame([item for key, subject in get_subject_data(subjecturl, "subject.json").items() for item in parser_page(get_raw_data(baseurl + key, subject), subject)])
    df.to_excel('2023qscn.xlsx', index=False)


if __name__ == '__main__':
    main()