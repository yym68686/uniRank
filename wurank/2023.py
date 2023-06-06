import requests

url='https://mallapi.wurank.net/RankApi/SearchApi/GetChineseUniDataPageList/chineseunidata'

def get_url(url):
    data = {
        "PageIndex": 1,
        "PageSize": 811,
        "filter": "intYear=2023",
        "sort": "intVictorOrder=0"
    }
    req = requests.post(url, json=data)
    req.encoding='utf-8'
    html = req.json()
    return html

dataset = get_url(url)
print(dataset)