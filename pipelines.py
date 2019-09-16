"""
Pipelines for the aggregation framework of MongoDB
"""
pipelines = [
    [
        {"$unwind": {"path": "$data.Bitcoin address", "preserveNullAndEmptyArrays": True}},
        {"$unwind": {"path": "$data.Ethereum address", "preserveNullAndEmptyArrays": True}},
        {"$unwind": {"path": "$data.BitcoinCash address", "preserveNullAndEmptyArrays": True}},
        {"$unwind": {"path": "$data.Litecoin address", "preserveNullAndEmptyArrays": True}},
        {"$unwind": {"path": "$data.Dogecoin address", "preserveNullAndEmptyArrays": True}},
        {"$unwind": {"path": "$data.Dash address", "preserveNullAndEmptyArrays": True}},
        {"$unwind": {"path": "$data.BitcoinSV address", "preserveNullAndEmptyArrays": True}},
        {"$unwind": {"path": "$data.Monero address", "preserveNullAndEmptyArrays": True}},

        {"$group": {"_id": {"User": "$data.Name"},
                    "btc": {"$addToSet": "$data.Bitcoin address"},
                    "eth": {"$addToSet": "$data.Ethereum address"},
                    "bch": {"$addToSet": "$data.BitcoinCash address"},
                    "ltc": {"$addToSet": "$data.Litecoin address"},
                    "doge": {"$addToSet": "$data.Dogecoin address"},
                    "dash": {"$addToSet": "$data.Dash address"},
                    "bsv": {"$addToSet": "$data.BitcoinSV address"},
                    "xmr": {"$addToSet": "$data.Monero address"},
                    "sources": {"$addToSet": "$data.Source"}
                    }},

        {"$project": {"_id": 0,
                      "user": "$_id.User",
                      "size btc": {"$size": "$btc"},
                      "size eth": {"$size": "$eth"},
                      "size bch": {"$size": "$bch"},
                      "size ltc": {"$size": "$ltc"},
                      "size doge": {"$size": "$doge"},
                      "size dash": {"$size": "$dash"},
                      "size bsv": {"$size": "$bsv"},
                      "size xmr": {"$size": "$xmr"},
                      "size sources": {"$size": "$sources"},
                      "or": {"$or": []}
                      }},

        {"$sort": {}},

        {"$match": {"or": {"$ne": False}}},

        {"$project": {
            "size btc": 0,
            "size eth": 0,
            "size bch": 0,
            "size ltc": 0,
            "size doge": 0,
            "size dash": 0,
            "size bsv": 0,
            "size xmr": 0,
            "size sources": 0,
            "or": 0
        }}

    ],
    [
        {"$unwind": {"path": "$data.Bitcoin address", "preserveNullAndEmptyArrays": True}},

        {"$group": {"_id": {"Address": "$data.Bitcoin address"},
                    "users": {"$addToSet": "$data.Name"},
                    "sources": {"$addToSet": "$data.Source"}
                    }},

        {"$project": {"_id": 0,
                      "Bitcoin address": "$_id.Address",
                      "users": 1,
                      "sources": 1,
                      "size users": {"$size": "$users"},
                      "size sources": {"$size": "$sources"}
                      }},

        {"$sort": {}},

        {"$project": {"size": 0}}
    ]
]
