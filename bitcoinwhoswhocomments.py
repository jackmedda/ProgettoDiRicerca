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
    data = getcommentsdata(page)

    dump(data, jsonfile, indent=4)


def getcommentsdata(page):
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
