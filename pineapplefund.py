from lxml import etree
import scraputils
import re
from json import dump

_url = "https://pineapplefund.org/"

"""File that scrapes the necessary data from PineappleFund site page"""

def main():
    filename = "pineapplefund.json"

    with open(filename, "w+") as jsonfile:
        data = []

        html = scraputils.gethtml(_url)

        result = re.findall(r"(?<=new Charity).*", html)

        data.append({
            "Organiztion": "Pineapple Fund",
            "Website": "https://pineapplefund.org",
            "Total sent (Dollars)": "55000000",
            "Transactions": [],
            "Bitcoin address": [],
            "Source": "Pineapple Fund",
            "Name": "Pineapple Fund"
        })

        for r in result:
            entry = {}
            r = r[2:-2]
            values = r.split("', '")
            entry["Organization"] = values[1].split('.')[0]
            entry["Website"] = values[0]
            entry["Total received (Dollars)"] = values[-1].split(', ')[-2]

            txs = re.search(r"\[.*\]", r)
            entry["Transactions"] = []
            for t in txs[0][1:-1].split(', '):
                entry["Transactions"].append(t[1:-1])
                data[0]["Transactions"].append(t[1:-1])

            entry["Bitcoin address"] = [""]  # Bitcoin addresses could be inserted only by hand
            entry["Source"] = "Pineapple Fund"
            entry["Name"] = entry["Organization"]

            data.append(entry)

        dump(data, jsonfile, indent=4)


if __name__ == "__main__":
    main()
