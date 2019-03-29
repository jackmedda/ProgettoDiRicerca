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
    users, startuser = load_data(filepath)
    with open(filepath, "w+") as jsonfile:
        if users:
            dump(users, jsonfile, indent=4)
        for u in range(startuser, LAST_BITCOINTALK_USER_21_03_2019_17_00_00):
            html = gethtml(url + str(u))
            page = etree.HTML(html)

            if not isemptypage(page):
                result = getfeatures(page)
                if result:
                    users[str(u)] = result
                    jsonfile.seek(0, 0)
                    dump(users, jsonfile, indent=4)

            sleep(1)


def getfeatures(page):
    result = {}
    b_toskip = [
        'Guest', 'News', 'Posts: ', 'Activity:', 'Position: ', 'Date Registered: ',
        'Last Active: ', 'Current Status: ', 'Gender: ', 'Age:', 'Local Time:'
    ]
    for b in page.iter('b'):
        if b.text is not None and b.text not in b_toskip:
            if b.text == "Email: ":
                email = b.getparent().getnext().getchildren()[0].text
                if email != "hidden":
                    result["Email"] = email
            elif b.text == "Signature:":
                attributes = []
                td = b.getparent().getparent().getnext().find('td/div')

                # Get all possible information in children tags
                for child in td.getchildren():
                    attributes.extend(child.values())
                    attributes.append(child.text)

                # Filters 'None' elements from attributes
                result["Signature"] = list(filter(None.__ne__, attributes))
            else:
                td = b.getparent().getnext()
                if td is not None:  # just td raise a FutureWarning, leave td is not None
                    if td.text:
                        result[b.text.split(':')[0]] = td.text

    return result


def getuserfeature(user):
    url = "https://bitcointalk.org/index.php?action=profile;u="
    return getfeatures(etree.HTML(gethtml(url + str(user))))


def gethtml(url):
    #  Bitcoin Talk wants User-Agent to work properly
    req = Request(url=url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/70.0.3538.77 Safari/537.36'})
    resource = urlopen(req)

    content = resource.read().decode(resource.headers.get_content_charset())
    resource.close()

    return content


def isemptypage(page):
    emptyuser = page.find("body//tr[@class='titlebg']/td")
    return emptyuser is not None and emptyuser.text == "An Error Has Occurred!"


def load_data(filepath):
    users = {}
    try:
        jsonfile = open(filepath, 'r')
        # Loads the json file and takes last key of the loaded dictionary
        users = load(jsonfile)
        startuser = int(list(users.keys())[-1]) + 1
        print(startuser)
        jsonfile.close()
    except IOError:
        startuser = FIRST_BITCOINTALK_USER

    return users, startuser


if __name__ == "__main__":
    main()
