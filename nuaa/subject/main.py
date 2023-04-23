import re
import os
import json
import pandas as pd
path = os.path.abspath(os.path.dirname(__file__)) + '/'

teather = pd.read_excel(path + 'nuaa_supervisor_information.xlsm')
teather_zh_list = teather['姓名'].tolist()
teather_en_list = teather['英文姓名'].tolist()
teather_de_list = teather['学院'].tolist()

# 把 teather_zh_list 和 teather_en_list 合并为字典
teather_name_dict = dict(zip(teather_zh_list, teather_en_list))
teather_de_dict = dict(zip(teather_zh_list, teather_de_list))

# 对 teather_dict 去重
teather_zh2en_dict = dict(zip(teather_name_dict.keys(), teather_name_dict.values()))
teather_en2zh_dict = dict(zip(teather_name_dict.values(), teather_name_dict.keys()))
teather_de_dict = dict(zip(teather_de_dict.keys(), teather_de_dict.values()))

# 专利
patent = pd.read_excel(path + 'patent.xlsx', sheet_name=1)
patent_list = patent['发明人（合并）'].tolist()
patent_list = list(set([i for j in [i.split('; ') for i in patent_list] for i in j]))

# 论文
article = pd.read_excel(path + 'article.xlsx', sheet_name=3)
article_list = article['论文'].tolist()
article_list = list(set([i for j in [re.findall(r'\[(.*?)\]', i) for i in article_list] for i in j]))
article_list = list(set([i for j in [i.split('; ') for i in article_list] for i in j]))

# 研究课题
subject = pd.read_excel(path + 'research_project.xlsx')
subject_list = subject['项目主持人'].tolist() + subject['参与者'].tolist()
subject_list = [i for i in subject_list if str(i) != 'nan']
subject_list = list(set([i for j in [i.split('；') for j in [i.split('; ') for i in subject_list] for i in j] for i in j]))
subject_list = [i for i in subject_list if str(i) != '']

teather_list = list(set(patent_list + article_list + subject_list))

with open(path + 'teather.json', 'w') as f:
    result = []
    for name in teather_list:
        if name in teather_en2zh_dict.keys():
            result.append({"英文名": name, "中文名": teather_en2zh_dict[name], "学院": teather_de_dict[teather_en2zh_dict[name]]})
        elif name in teather_zh2en_dict.keys():
            result.append({"英文名": teather_zh2en_dict[name], "中文名": name, "学院": teather_de_dict[name]})
        else:
            print(name, 'not found')
    result = [dict(t) for t in set([tuple(d.items()) for d in result])]
    f.write(json.dumps(result, ensure_ascii=False, indent=4))

# 把json文件转换为excel文件
with open(path + 'teather.json', 'r') as f:
    teather = json.load(f)
teather = pd.DataFrame(teather)
teather.to_excel(path + '智能科学与技术--南航学者情况.xlsx', index=False)
