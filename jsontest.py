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
    "wauholland.json"
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
    Merge
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
