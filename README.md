# uniRank

## 简介

世界主流机构大学排名爬虫：qs，usnews，软科

南航所有学院导师研究方向爬虫

一键部署到 Replit：

[![Run on Repl.it](https://replit.com/badge/github/yym68686/uniRank)](https://replit.com/new/github/yym68686/uniRank)

安装 python 包依赖

```
pip install -r requirements.txt --index-url https://pypi.python.org/simple/
```

## QS 世界大学数据排名

- 2022qs.py 爬取 2022 数据
- 2023qs.py 爬取 2023 数据

## 软科

### 2022 科软世界大学学术排名 arwu

kr.py 下载科软世界大学学术排名（Academic Ranking of World Universities，简称ARWU）。

json 在线转换 excel

[在线JSON转Excel工具 - UU在线工具 (wejson.cn)](https://wejson.cn/json2excel/)

### 2022 软科中国大学专业排名 bcsr

寻找 api 的方法：在浏览器开发者工具里网络中查找 http://127.0.0.1:8651 ，后面跟的 url 就是 API 接口。

中国大学专业排名 API 接口

https://www.shanghairanking.cn/api/pub/v1/bcsr/rank?target_yr=2022&subj_code=0101

学科代码 API 接口

https://www.shanghairanking.cn/api/pub/v1/bcsr/subj?year=2022

### 2022 软科世界一流学科排名

网址：

https://www.shanghairanking.cn/rankings/gras/2022

api：

https://www.shanghairanking.cn/api/pub/v1/gras/rank?year=2022&subj_code=RS0101

### 2023 软科中国大学排名

主榜数据：

https://www.heywhale.com/mw/dataset/64255ba434db799a8ab0ff5b/file

## usnews 世界大学数据排名

2022 usnews 大学排名网址：https://www.usnews.com/education/best-global-universities/rankings

api：https://www.usnews.com/education/best-global-universities/search?format=json&page=1

利用 js 脚本下载 json 数据：

```javascript
let items = [];
for(let i = 1; i <= 217; i++) {
    result = await fetch(`https://www.usnews.com/education/best-global-universities/search?format=json&page=${i}`, {
  "headers": {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "sec-ch-ua": "\"Chromium\";v=\"106\", \"Google Chrome\";v=\"106\", \"Not;A=Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "\"Android\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin"
  },
  "referrer": "https://www.usnews.com/",
  "referrerPolicy": "origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "include"
});
    uni = await result.json();
    items.push(...uni['items']);
}
let blob  = new Blob([JSON.stringify(items)]);
var a = document.createElement('a');
a.download = "uni.json";
a.href = window.URL.createObjectURL(blob);
a.click();
```

- 多下载几次，有时候下载数据不对
- 在开发者工具打开控制台下载
- 2022 一共 2165 个学校，最后总数据不是 2165，就是下载错误，多尝试几次
