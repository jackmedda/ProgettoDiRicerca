pipelines = [
    [
        {"$group": {"_id": {"Name": "$data.Name"}, "count": {"$sum": 1}}},
        {"$match": {"_id.Name": {"$ne": "null"}}},
        {"$sort": {"count": -1}}
    ],
    [
        {"$unwind": {"path": "$data.Bitcoin address", "preserveNullAndEmptyArrays": "true"}},
        {"$unwind": {"path": "$data.Ethereum address", "preserveNullAndEmptyArrays": "true"}},
        {"$unwind": {"path": "$data.BitcoinCash address", "preserveNullAndEmptyArrays": "true"}},
        {"$unwind": {"path": "$data.Litecoin address", "preserveNullAndEmptyArrays": "true"}},
        {"$unwind": {"path": "$data.Dogecoin address", "preserveNullAndEmptyArrays": "true"}},
        {"$unwind": {"path": "$data.Dash address", "preserveNullAndEmptyArrays": "true"}},
        {"$unwind": {"path": "$data.BitcoinSV address", "preserveNullAndEmptyArrays": "true"}},
        {"$unwind": {"path": "$data.Monero address", "preserveNullAndEmptyArrays": "true"}},

        {"$group": {"_id": {"User": "$data.Name"},
                    "btc": {"$addToSet": "$data.Bitcoin address"},
                    "eth": {"$addToSet": "$data.Ethereum address"},
                    "bch": {"$addToSet": "$data.BitcoinCash address"},
                    "ltc": {"$addToSet": "$data.Litecoin address"},
                    "doge": {"$addToSet": "$data.Dogecoin address"},
                    "dash": {"$addToSet": "$data.Dash address"},
                    "bsv": {"$addToSet": "$data.BitcoinSV address"},
                    "xmr": {"$addToSet": "$data.Monero address"}
                    }},

        {"$match": {"_id.User": {"$ne": "null"}}},

        {"$project": {"_id": 0,
                      "user": "$_id.User",
                      "btc": 1,
                      "eth": 1,
                      "bch": 1,
                      "ltc": 1,
                      "doge": 1,
                      "dash": 1,
                      "bsv": 1,
                      "xmr": 1,
                      "size1": {"$size": "$btc"},
                      "size2": {"$size": "$eth"},
                      "size3": {"$size": "$bch"},
                      "size4": {"$size": "$ltc"},
                      "size5": {"$size": "$doge"},
                      "size6": {"$size": "$dash"},
                      "size7": {"$size": "$bsv"},
                      "size8": {"$size": "$xmr"},
                      }},

        {"$sort": {}},

        {"$project": {
            "size1": 0,
            "size2": 0,
            "size3": 0,
            "size4": 0,
            "size5": 0,
            "size6": 0,
            "size7": 0,
            "size8": 0
        }}

    ],
    [
        {"$unwind": "$data.Bitcoin address"},

        {"$group": {"_id": {"Address": "$data.Bitcoin address"},
                    "users": {"$addToSet": "$data.Name"},
                    "source": {"$addToSet": "$data.Source"}
                    }},

        {"$project": {"_id": 0, "Bitcoin address": "$_id.Address", "users": 1, "source": 1,
                      "size": {"$size": "$users"}}},

        {"$sort": {"size": -1}},

        {"$project": {"size": 0}}
    ]
]
