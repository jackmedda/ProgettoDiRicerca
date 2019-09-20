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

from lxml import etree
import scraputils
from addrfilter import findalladdresses
from json import dump
import validators

_url = "https://bitcoinwhoswho.com/blog/2016/02/29/bitcoin-donation-address-rankings/"


def main():
    filename = "bitcoinwhoswhocomcommentsaddresses2.json"

    with open(filename, "w+") as jsonfile:
        html = scraputils.gethtml(_url)
        page = etree.HTML(html)

        datatojson(page, jsonfile)


def datatojson(page, jsonfile):
    """
    Call the function to get scraped data from page and save it in a json file
    :param page: html of the page to be scraped
    :param jsonfile: path of the json
    :return:
    """
    data = getcommentsdata(page)

    dump(data, jsonfile, indent=4)


def getcommentsdata(page):
    """
    Scrapes data from the comments of the article in page
    :param page: html of the page to be scraped
    :return: scraped data
    """
    data = []

    commentlist = page.find('body/div/div[@id="main"]/div[@id="primary"]/div/div[@id="comments"]/ol')

    for comment in commentlist:
        if isinstance(comment.tag, str):  # Avoid to iterate on html comments
            commentdata = {}
            author = comment.find('article/footer/div[@class="comment-author vcard"]/b')
            if author.text:
                commentdata["Name"] = author.text
            else:
                a_author = author.getchildren()[0]
                commentdata["Name"] = a_author.text
                authorurl = a_author.get("href")

                if type(validators.url(authorurl)) != validators.utils.ValidationFailure:  # if it is a valid url
                    commentdata["Url"] = authorurl

            content = comment.find('article/div')

            # Retrieve addresses from plain html (so find addresses in both attributes and text)
            addrs = findalladdresses(etree.tostring(content, encoding=str, method="html"))

            if addrs.__len__() != 0:
                # Retrieve only the text without tags
                contenttext = " ".join(etree.tostring(content, encoding=str, method="text").split())

                commentdata["Comment"] = contenttext

                commentdata["Source"] = "BitcoinWhosWho: Comments"

                for addr in addrs:
                    if addr[0] in commentdata:
                        commentdata[addr[0]].append(addr[1])
                    else:
                        commentdata[addr[0]] = [addr[1]]

                data.append(commentdata)

    return data


if __name__ == "__main__":
    main()
