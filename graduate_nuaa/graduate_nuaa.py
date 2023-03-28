import os
import json
import requests
import pandas as pd

dirpath = os.path.abspath(os.path.dirname(__file__))
# json 数据
url = "http://graduate.nuaa.edu.cn/gmis5/dsfc/getdsxxpage"
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
}

def getJSON():
    xyList = json.load(open(dirpath + "/学院.json", "r", encoding = 'utf-8'))
    result = {}
    for id, xyName in xyList.items():
        if not os.path.exists(dirpath + f"/{xyName}.json"):
            r = requests.post(url, headers=headers,data={'xsbh': '{}'.format(id)})
            with open(dirpath + f"/{xyName}.json", "w", encoding = 'utf-8') as f:
                f.write(r.text)
        with open(dirpath + f"/{xyName}.json", "r", encoding = 'utf-8') as f:
            rawdata = json.load(f)
        dict = []
        for i in rawdata["yjxk"]:
            if "zy" not in i and (i["bdList"] or i["sdList"]):
                dict.append(i)
            if "zy" in i:
                dict+=[j for j in i["zy"] if j["bdList"] or j["sdList"]]
        for i in dict:
            for j in i["bdList"] + i["sdList"]:
                result.setdefault(j["dsxm"], {}).setdefault(f"{xyName}", []).append(i["xkmc"])
        print("=>", xyName)
    with open(dirpath + "/result.json", "w", encoding = 'utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    return result

def main():
    data = getJSON()
    # new_dict = {}
    # for TeacherName, TeacherInfo in result.items():
    #     for CollegeName, subjectList in TeacherInfo.items():
    #         for zyName in subjectList:
    #             new_dict.setdefault(TeacherName, {}).setdefault(CollegeName + '_' + zyName, []).extend(subjectList[zyName])
    ans = []
    for name, departments in data.items():
        result = []
        result.append(name)
        for department, courses in departments.items():
            result.append(department)
            result.extend(courses)
        ans.append(result)
    
    df = pd.DataFrame(ans)
    df = pd.DataFrame(df.values.tolist())
    df.to_excel(dirpath + '/result.xlsx')

    # df = pd.DataFrame(new_dict).T
    # df.to_excel(dirpath + '/result.xlsx')

if __name__ == '__main__':
    main()