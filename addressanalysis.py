from pymongo import MongoClient
from time import sleep
import json
import requests

base_api = "https://api.blockchair.com/"
api_path_address = "/dashboards/address/"
api_path_tx = "/dashboards/transactions/"

groups = []
with open('AnalisiDati.txt', 'r') as data:
    file = data.readlines()
    gr = file[-34:]
    gr = [x.split(':', 1)[0][1:-1].split(', ') for x in gr if x != '\n']
    for i, x in enumerate(gr):
        for j, y in enumerate(x):
            gr[i][j] = y + ' address'
    groups = gr

database = None
try:
    connection = MongoClient('mongodb://localhost:27017')
    database = connection['research']
except ConnectionError:
    connection = None

data = []
for gr in groups:
    query = [
        {"$group":
             {"_id": {}}},
        {"$project": {
            "_id": 0,
            "Bitcoin address": "$_id.Bitcoin address",
            "Ethereum address": "$_id.Ethereum address",
            "Litecoin address": "$_id.Litecoin address",
            "Dogecoin address": "$_id.Dogecoin address",
            "Dash address": "$_id.Dash address"
        }},
        {"$match": {"$and": []
        }}
    ]
    for x in gr:
        query[0]["$group"]["_id"][x] = "$data." + x
        query[2]["$match"]["$and"].append({x: {"$ne": None}})

    doc = []
    if connection:
        doc = list(database['data2'].aggregate(query))

    group_data = []
    for res in doc:
        for addrs in res:
            for addr in res[addrs]:
                response = requests.get(base_api + addrs.split(' ')[0].lower() + api_path_address + addr)
                group_data.append(response.json())
                sleep(2)
    data.append(group_data)

with open("blockdata.json", "w") as f:
    json.dump(data, f, indent=4)
