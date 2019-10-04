# This software is distributed under MIT/X11 license
# Copyright (c) 2019 Giacomo Medda - University of Cagliari
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

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
        addr_data = []
        for addrs in res:
            for addr in res[addrs]:
                response = requests.get(base_api + addrs.split(' ')[0].lower() + api_path_address + addr)
                addr_data.append(response.json())
                sleep(2)
        group_data.append(addr_data)
    data.append(group_data)

with open("blockdata.json", "w") as f:
    json.dump(data, f, indent=4)
