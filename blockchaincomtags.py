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
    """
    Handles the crawling of Blockchain.com domain
    :return:
    """
    for file, url in _url.items():
        filename = file + ".json"
        data, startoffset = scraputils.load_data(filename, 50)

        # from first page it's possible to get the endoffset
        html = scraputils.gethtml(url + "0")
        page = etree.HTML(html)
        endoffset = int(page.find("body/div/div/ul/li[last()-1]/a").values()[0].split('=')[2])

        with open(filename, "w+") as jsonfile:
            if data:
                dump(data, jsonfile, indent=4)
            for u in range(startoffset, endoffset + 1, 50):
                html = scraputils.gethtml(url + str(u))
                page = etree.HTML(html)

                datatojson(page, jsonfile, data, u)

                sleep(1)


def datatojson(page, jsonfile, data, u):
    """
    Dumps data as a json file
    :param page: html page to be scraped
    :param jsonfile: path where to save the json
    :param data: data to be saved in the json
    :param u: represents an offset that shifts of 50 for each page, because of for each page 50 values are shown
    :return:
    """
    data.update(getdata(page))

    if str(u - 50) in data:
        del data[str(u - 50)]

    data[str(u)] = []
    jsonfile.seek(0, 0)
    dump(data, jsonfile, indent=4)


def getdata(page):
    """
    Scrapes the data from the page taken as parameter
    :param page: page to be scraped
    :return: scraped data
    """
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
