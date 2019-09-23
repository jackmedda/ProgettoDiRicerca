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

import json

jsons = [
    "abuse_reports_bitcoin2.json",
    "Bitcoin-OTC2.json",
    "blockchaincomsubmittedlinks2.json",
    "bitcoinwhoswhocombitcoindonationaddressranking2.json",
    "bitcoinwhoswhocomcommentsaddresses2.json",
    "blockchaincombitcoinOTCprofiles2.json",
    "blockchaincombitcointalkprofiles2.json",
    "blockchaincomsignedmessages2.json",
    "blockchaincomsubmittedlinks2.json",
    "pineapplefund.json",
    "wauholland.json",
    "BitcoinTalkUsers.json"
]

new_addresses = ["Bitcoin address", "Ethereum address", "BitcoinCash address", "Litecoin address", "Dogecoin address", "Dash address", "BitcoinSV address", "Monero address",]
old_addresses = ["Bitcoin Address", "Ethereum Address", "BitcoinCash Address", "Litecoin Address", "Dogecoin Address", "Dash Address", "BitcoinSV Address", "Monero Address"]
_tags = ["Name", "Tag", "abuser", "nick", "Organization", "Project"]


def address_to_array_address():
    """
    Used to make the addresses fields as arrays of addresses for formatting purposes
    :return:
    """
    for lit in jsons:
        with open(lit, "r") as _file:
            data = json.load(_file)
            for x in data:
                for a in new_addresses:
                    if a in x:
                        if type(x[a]) != list:
                            x[a] = [x[a]]
        with open(lit, "w+") as f:
            json.dump(data, f, indent=4)


def data_json_composer():
    """
    Merge all the jsons adding the field "Name" with a value equals to the field called as one in "_tags" array.
    All this data are then added to a "data" object, and so each document contains an ID and the object "data"
    :return:
    """
    lit = "data.json"
    result = []
    i = 1
    for j in jsons:
        with open(j, "r") as file:
            data = json.load(file)
            for x in data:
                if "Bitcoin Donation Address" in x:
                    x["Bitcoin address"] = x["Bitcoin Donation Address"]
                    del x["Bitcoin Donation Address"]
                for t in _tags:
                    if t in x:
                        x["Name"] = x[t]
                result.append({
                    "ID": i,
                    "data": x
                })
                i += 1
    with open(lit, "w") as f:
        json.dump(result, f, indent=4)
