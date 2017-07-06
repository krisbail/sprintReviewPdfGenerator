# coding: utf8
# encoding=utf8

import requests
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf8')


url = "https://www.forge.orange-labs.fr:443/api/tokens"
payload = {"username":"coib7363", "password":"Grand31**"}
headers = {'content-type': 'application/json'}

#r = requests.post(url, data=json.dumps(payload), headers=headers)

#print r.status_code
#print r.headers
#print r.json()
# retour : {u'token': u'9ddf52118bf00b61f7ad94be90d4f077', u'user_id': 9680, u'uri': u'tokens/9ddf52118bf00b61f7ad94be90d4f077'}


headers["X-Auth-Token"] = u'851f56bfecf278046c7e600f995686f1'
headers["X-Auth-UserId"] = 9680

url = "https://www.forge.orange-labs.fr:443/api/artifacts/340574?values_format=collection"
#url = "https://www.forge.orange-labs.fr:443/api/trackers/16993/artifacts?values=all&limit=20&expert_query=mle%20%3D%20'Beluga'%20AND%20status_id%20%3D%20'new'%20AND%20target_sprint_1%20%3D%20'Phoenix%20R1S27'&order=asc"

#url = "https://www.forge.orange-labs.fr:443/api/trackers/16993/artifacts?values=all&limit=2&expert_query=mle%20%3D%20'Beluga'%20AND%20status_id%20%3D%20'new'"
payload = {"values": "all", "limit": 100, "expert_query":  "mle='Beluga' AND status_id='new'"}
url = "https://www.forge.orange-labs.fr:443/api/trackers/16993/artifacts"

r = requests.get(url, headers=headers, params=payload)
print r.url
print r.status_code
print r.headers
#print r.json()

bugs = r.json()

map_key_bug_debt = {
    'aid': 'FORGE id',
    'title': 'summary',
    'Category': 'component',
    'status': 'status_id',
    'Urgency': 'urgency',
    'Severity': 'severity'
}

def completeBug(myBug, bug):
    for val in bug["values"]:
        if val["field_id"] in [86165, 86166, 133311]:
            value = [{"label", val["value"]}] if "value" in val else val["values"]
            key_label = map_key_bug_debt[val["label"]]
            #myBug[key_label] = value[0]["label"].encode('utf-8') if len(value) > 0 else ""
            myBug[key_label] = value[0]["label"] if len(value) > 0 else ""


with open('names.csv', 'w') as csvfile:
    fieldnames = ['FORGE id', 'status_id', 'summary', 'component', 'severity', 'urgency']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()
    for bug in bugs:
        objectBug = {}
        objectBug["FORGE id"] = bug["id"]
        objectBug["status_id"] = bug["status"]
        objectBug["summary"] = bug["title"]
        completeBug(objectBug, bug)
        #print objectBug
        writer.writerow(objectBug)


