from urllib.request import urlopen, Request
from lxml import etree
from bitcoinaddressvalidator import check_bc
from time import sleep
from json import dump, load
from addrfilter import findalladdresses

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
            datatojson(url, jsonfile, users, u)


def datatojson(url, jsonfile, users, u):
    html = gethtml(url + str(u))
    page = etree.HTML(html)

    # This function permits to restart the program from the last checked user and not last user with some data
    def addlastcheckeduser(data):
        if str(u - 1) in users:
            if not users[str(u - 1)]:
                del users[str(u - 1)]
        users[str(u)] = data
        jsonfile.seek(0, 0)
        dump(users, jsonfile, indent=4)

    if not isemptypage(page):
        result = getfeatures(page)
        # join concatenate all strings of the values of the dictionary 'result'
        addresses = tupleset_to_dict(findalladdresses(' '.join(result.values())))
        # Users with no addresses are not useful
        if result and addresses:
            result.update(addresses)
            # print(result)
            addlastcheckeduser(result)
            jsonfile.seek(0, 0)
            dump(users, jsonfile, indent=4)
        else:
            addlastcheckeduser([])
    else:
        addlastcheckeduser([])

    sleep(1)


def finddatabyuserid(user):
    url = "https://bitcointalk.org/index.php?action=profile;u="
    html = gethtml(url + str(user))
    page = etree.HTML(html)

    if not isemptypage(page):
        result = getfeatures(page)
        print(result)
        # join concatenate all strings of the values of the dictionary 'result'
        addresses = tupleset_to_dict(findalladdresses(' '.join(result.values())))
        print(addresses)
        # Users with no addresses are not useful
        if result and addresses:
            result.update(addresses)
            print(result)


def getfeatures(page):
    '''
    The getfeatures method takes the lxml ElementTree root of the web page and extract useful information from it.
    Here it is necessary to insert the implementation to extract all data from the web page.

    :param page: the page need to be analysed to extract useful information
    :return: an associative array containing the information that is useful for a particular purpose
    '''
    result = {}
    # <b> tags to not consider
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

                attributes.append(td.text)

                # Get all possible information in children tags
                for child in td.getchildren():
                    attributes.extend(child.values())
                    attributes.append(child.text)

                # Filters 'None' elements from attributes
                if attributes:
                    # Signature as a long string with each useful value separated by a comma
                    result["Signature"] = ', '.join(list(item for item in attributes if item and item != 'ul'))
            elif b.text == "Website: ":
                td = b.getparent().getnext().getchildren()[0]
                website = td.values()[0]
                if website:  # if href contains something
                    result["Website"] = (td.text if td.text else "") + " " + website
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
    startuser = 0
    try:
        jsonfile = open(filepath, 'r')
        # Loads the json file and takes last key of the loaded dictionary
        if jsonfile:
            users = load(jsonfile)
            startuser = int(list(users.keys())[-1]) + 1
            if not users[str(startuser-1)]:
                del users[str(startuser-1)]

        jsonfile.close()
    except IOError:
        startuser = FIRST_BITCOINTALK_USER

    return users, startuser


def tupleset_to_dict(addresses):
    result = {}
    for x in addresses:
        result[x[0]] = x[1]
    return result


if __name__ == "__main__":
    main()
