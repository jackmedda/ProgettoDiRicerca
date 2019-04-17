from webutils import gethtml
from lxml import etree
from json import load, dump
from os import stat

_url = {
    "urlbitcointalkprofiles": "https://www.blockchain.com/btc/tags?filter=2",
    "urlbitcoinOTCprofiles": "https://www.blockchain.com/btc/tags?filter=4",
    "urlsubmittedlinks": "https://www.blockchain.com/btc/tags?filter=8",
    "urlsignedmessages": "https://www.blockchain.com/btc/tags?filter=16"
}


def main():
    for file, url in _url.items():
        data, startoffset = load_data(file + ".json")

        if startoffset != 0:
            url = url + "&offset=" + str(startoffset)

        with open(filepath, "w+") as jsonfile:
            if data:
                dump(data, jsonfile, indent=4)
            for u in range(startoffset, endoffset, 50):
                html = gethtml(url)
                page = etree.HTML(html)
                datatojson(_url, jsonfile, users, u)
                sleep(1)


def load_data(filepath):
    data = {}
    startoffset = 0
    try:
        jsonfile = open(filepath, 'r')
        # Loads the json file and takes last key of the loaded dictionary
        if jsonfile:
            if stat(jsonfile.name).st_size != 0:
                users = load(jsonfile)
                startoffset = int(list(users.keys())[-1]) + 1
                if not users[str(startoffset-1)]:
                    del users[str(startoffset-1)]

        jsonfile.close()
    except IOError:
        pass

    return data, startoffset


if __name__ == "__main__":
    main()
