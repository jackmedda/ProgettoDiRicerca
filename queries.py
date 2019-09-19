"""
Queries for the database of MongoDB
"""
queries = [
    [
        {"$group": {"_id": {}
                    }},

        {"$project": {"_id": 0,
                      "or": {"$or": []}
                      }},

        {"$sort": {}},

        {"$match": {"or": {"$ne": False}}},

        {"$project": {
            "or": 0
        }}
    ]
]
