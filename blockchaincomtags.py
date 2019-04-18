import scraputils
from lxml import etree
from addrfilter import findalladdresses
from json import dump
from time import sleep
import itertools

_url = {
    "blockchaincombitcointalkprofiles": "https://www.blockchain.com/btc/tags?filter=2&offset=",
    "blockchaincombitcoinOTCprofiles": "https://www.blockchain.com/btc/tags?filter=4&offset=",
    "blockchaincomsubmittedlinks": "https://www.blockchain.com/btc/tags?filter=8&offset=",
    "blockchaincomsignedmessages": "https://www.blockchain.com/btc/tags?filter=16&offset="
}


def main():
    for file, url in _url.items():
        filepath = file + ".json"
        data, startoffset = scraputils.load_data(filepath)

        # from first page it's possible to get the endoffset
        html = scraputils.gethtml(url + "0")
        page = etree.HTML(html)
        endoffset = int(page.find("body/div/div/ul/li[last()-1]/a").values()[0].split('=')[2])

        with open(filepath, "w+") as jsonfile:
            if data:
                dump(data, jsonfile, indent=4)
            for u in range(startoffset, endoffset, 50):
                html = scraputils.gethtml(url + str(u))
                page = etree.HTML(html)

                datatojson(page, jsonfile, data, u)

                sleep(1)


def datatojson(page, jsonfile, data, u):
    data.update(getdata(page))

    if str(u - 50) in data:
        del data[str(u - 50)]

    data[str(u)] = []
    jsonfile.seek(0, 0)
    dump(data, jsonfile, indent=4)


def getdata(page):
    datatable = page.find('body/div/table/tbody')
    data = {}
    # the verification is represented by an image of a green tick or a red cross in the site
    verified = {'/Resources/green_tick.png': True, '/Resources/red_cross.png': False}

    keys = ['Tag', 'Link', 'Verified']
    for tr in datatable:
        address = ""
        dataaddress = {}
        for k, td in enumerate(tr):
            content = (list(td)[0])
            if k == 0:
                address = content.text
                addresstype = findalladdresses(address)
                if addresstype:
                    dataaddress["Type"] = addresstype.pop()[0]
            else:
                if content.text:
                    dataaddress[keys[k-1]] = content.text
                if content.get('src'):
                    dataaddress[keys[k-1]] = verified[content.get('src')]
        data[address] = dataaddress
    return data


if __name__ == "__main__":
    main()
