from urllib.request import urlopen, Request
from lxml import etree
from bitcoinaddressvalidator import check_bc
from time import sleep


def main():
    url = "https://bitcointalk.org/index.php?action=profile;u="

    filepath = "BitcoinTalkScrapingResult.txt"
    with open(filepath, "w") as txt:
        for u in range(4, 100):#2562718):
            sleep(1)
            html = getHTML(url + str(u))
            page = etree.HTML(html)

            if not isemptypage(page):
                txt.write(str(u) + ' ' + getfeatures(page) + '\n')


def isemptypage(page):
    emptyuser = page.find("body//tr[@class='titlebg']/td")
    return emptyuser is not None and emptyuser.text == "An Error Has Occurred!"


def getfeatures(page):
    result = ''
    for b in page.iter('b'):
        if b.text in ('Bitcoin address: ', 'Name: ', 'Location:', 'Signature:'):
            if b.text == "Signature:":
                td = b.getparent().getparent().getnext().find('td/div')
            else:
                td = b.getparent().getnext()
            if td is not None:
                if td.text is not None:
                    #if b.text == 'Bitcoin address: ':
                        #if check_bc(td.text):
                            #print(b.text + td.text)
                    #else:
                        if b.text in ('Location:', 'Signature:'):
                            print(b.text + ' ' + td.text)
                        else:
                            print(b.text + td.text)
                else:
                    print(b.text)

    return result


def getHTML(url):
    req = Request(url=url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
    resource = urlopen(req)

    content = resource.read().decode(resource.headers.get_content_charset())
    resource.close()

    return content


if __name__ == "__main__":
    main()