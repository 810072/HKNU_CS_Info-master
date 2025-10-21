import json
with open('json/data.json', 'r', encoding='utf-8') as f:
    data_json = json.load(f)
if "asdf" in data_json['deleted']:
    print(data_json['deleted'])