import json

USER_DATA_GROUP = {'Name': 'Zara'}
with open('NKNCN.json') as json_data:
    d = json.load(json_data)
    for item in d:
        print(type(item["id"]))
        USER_DATA_GROUP[item['id']] = "0"

with open('NKN.json') as json_data:
    d = json.load(json_data)
    for item in d:
        USER_DATA_GROUP[item['id']] = "0"

print(395368493 in USER_DATA_GROUP)