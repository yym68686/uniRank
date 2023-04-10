import os
import json
from operator import itemgetter

dirpath = os.path.abspath(os.path.dirname(__file__))
with open(dirpath + "/uni.json", "r", encoding = 'utf-8') as f:
    dataset = json.load(f)
dict = []
idx = len(dataset)
for i in range(idx):
    Rank = dataset[i]['ranks'][0]['value']
    univName = dataset[i]['name']
    Country = dataset[i]['country_name']
    City = dataset[i]['city']
    Score = dataset[i]['stats'][0]['value']
    Enrollment = dataset[i]['stats'][1]['value']
    dict.append({
                "Rank": Rank,
                "University": univName,
                "Country": Country,
                "City": City,
                "Global Score": Score,
                "Enrollment": Enrollment
                })
with open(dirpath + "/usnews.json", "w", encoding = 'utf-8') as f:
    json.dump(dict, f, ensure_ascii=False, indent=4)