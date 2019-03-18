from urllib.request import urlopen, Request
from lxml import etree

def main():
    url = "https://bitcointalk.org/index.php?action=profile;u=60001"
    html = getHTML(url)

    page = etree.HTML(html)

    for b in page.getiterator('b'):
        if b.text in ('Bitcoin address: ', 'Name: ', 'Location: ', 'Signature: '):
            td = b.getparent().getnext()
            if td is not None:
                if td.text is not None:
                    print(b.text + td.text)
    #for table_row in page.findall("body//table[@cellpadding='2']/tr/td"):
    #    print(table_row.tag)
    #    print(table_row.text)

    #print(page.find("/body/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody"))
    #print (page.findtext("address"))

    #filepath = "BitcoinTalkScrapingResult.txt"
    #soup = BeautifulSoup("")
    #with open(filepath, "w") as txt:è
    #    for u in range(4,2562718):
    #        print ""


def getHTML(url):
    req = Request(url=url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
    fp = urlopen(req)

    bytepage = fp.read()

    htmlpage = bytepage.decode("utf8")
    fp.close()

    return htmlpage


if __name__ == "__main__":
    main()