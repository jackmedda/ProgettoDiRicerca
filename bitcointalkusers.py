from urllib.request import urlopen, Request
from lxml import etree
from bitcoinaddressvalidator import check_bc
from time import sleep
from json import dump, load

FIRST_BITCOINTALK_USER = 1
LAST_BITCOINTALK_USER_21_03_2019_17_00_00 = 2566477


def main():
    url = "https://bitcointalk.org/index.php?action=profile;u="

    filepath = "BitcoinTalkUsers.json"
    users, startuser = loaddata(filepath)
    with open(filepath, "w+") as jsonfile:
        for u in range(startuser, LAST_BITCOINTALK_USER_21_03_2019_17_00_00):
            html = getHTML(url + str(u))
            page = etree.HTML(html)

            if not isemptypage(page):
                users[str(u)] = getfeatures(page)
                jsonfile.seek(0, 0)
                dump(users, jsonfile, indent=4)

            sleep(1)


def isemptypage(page):
    emptyuser = page.find("body//tr[@class='titlebg']/td")
    return emptyuser is not None and emptyuser.text == "An Error Has Occurred!"


def getfeatures(page):
    result = {}
    for b in page.iter('b'):
        if b.text in ('Bitcoin address: ', 'Name: ', 'Location:', 'Signature:'):
            if b.text == "Signature:":
                td = b.getparent().getparent().getnext().find('td/div')
            else:
                td = b.getparent().getnext()
            if td is not None:
                if td.text is not None:
                    # if b.text == 'Bitcoin address: ':
                        # if check_bc(td.text):
                            # print(b.text + td.text)
                    # else:
                        result[b.text.split(':')[0]] = td.text

    return result


def getHTML(url):
    req = Request(url=url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
    resource = urlopen(req)

    content = resource.read().decode(resource.headers.get_content_charset())
    resource.close()

    return content


def loaddata(filepath):
    jsonfile = open(filepath, 'r')
    users = {}
    try:
        # Loads the json file and takes last key of the loaded dictionary
        users = load(jsonfile)
        startuser = int(list(users.keys())[-1])
        print(startuser)
    except:
        startuser = FIRST_BITCOINTALK_USER

    jsonfile.close()

    return users, startuser


if __name__ == "__main__":
    main()
