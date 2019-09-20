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
from time import sleep
from json import dump
from addrfilter import findalladdresses

LAST_BITCOINTALK_USER_21_03_2019_17_00_00 = 2566477

_url = "https://bitcointalk.org/index.php?action=profile;u="


def main():
    """
    Loads the data from the json and continues to scrape data from the profile pages
    :return:
    """
    filename = "BitcoinTalkUsers.json"
    users, startuser = scraputils.load_data(filename, 1)

    with open(filename, "w+") as jsonfile:
        if users:
            dump(users, jsonfile, indent=4)
        for u in range(startuser, LAST_BITCOINTALK_USER_21_03_2019_17_00_00 + 1):
            html = scraputils.gethtml(_url + str(u))
            page = etree.HTML(html)

            datatojson(page, jsonfile, users, u)

            sleep(0.3)


def datatojson(page, jsonfile, users, u):
    """
    Dumps data as a json file if data has valid addresses and substitute data of previous user
    if no significant data has been extracted
    :param page: page to be scraped
    :param jsonfile: path of json
    :param users: dict containing all data of the json and updated for each new found data
    :param u: current user id
    :return:
    """
    # This function permits to restart the program from the last checked user and not last user with some data
    def addlastcheckeduser(data):
        if users:
            if str(u - 1) == users[-1]["BitcoinTalkID"]:
                if "Name" not in users[-1]:
                    del users[-1]
        data.update({"BitcoinTalkID": str(u), "Source": "BitcoinTalk"})
        users.append(data)
        jsonfile.seek(0, 0)
        dump(users, jsonfile, indent=4)

    if not isemptypage(page):
        result = getfeatures(page)
        # join concatenate all strings of the values of the dictionary 'result'
        addresses = scraputils.tupleset_to_dict_of_sets(findalladdresses(' '.join(result.values())))
        # Users with no addresses are not useful
        if result and addresses:
            result.update(addresses)
            # print(result)
            addlastcheckeduser(result)
        else:
            addlastcheckeduser({})
    else:
        addlastcheckeduser({})


def getfeatures(page):
    """
    The getfeatures method takes the lxml ElementTree root of the web page and extract useful information from it.
    Here it is necessary to insert the implementation to extract all data from the web page.

    :param page: the page need to be analysed to extract useful information
    :return: an associative array containing the information that is useful for a particular purpose
    """
    result = {}
    # <b> tags to consider
    b_tochoose = [
        'Name: ', 'Website: ', 'Bitcoin Address: ', 'Location:', 'Signature:', 'Skype: ',
        'Other contact info: ', 'Email: '
    ]
    for b in page.iter('b'):
        if b.text is not None and b.text in b_tochoose:
            if b.text == "Email: ":
                email = b.getparent().getnext().getchildren()[0].text
                if email != "hidden":
                    result["Email"] = email
            elif b.text == "Signature:":
                attributes = []
                td = b.getparent().getparent().getnext().find('td/div')

                if td.text:
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
    """
    Get data related to a user given user id. Primarily a test function
    :param user: user id (int)
    :return: a dictionary with data of the user
    """
    page = etree.HTML(scraputils.gethtml(_url + str(user)))
    if not isemptypage(page):
        return getfeatures(page)
    else:
        print("Empty profile")
        return None


def getfeatureaddresses(feature):
    """
    Get the addresses from a dictionary of features
    :param feature: dict of features
    :return: a dict of sets containing the addresses
    """
    return scraputils.tupleset_to_dict_of_sets(findalladdresses(' '.join(feature.values())))


def isemptypage(page):
    """
    Check if a user profile page is empty
    :param page: page to be checked
    :return: True if page is empty
    """
    emptyuser = page.find("body//tr[@class='titlebg']/td")
    return emptyuser is not None and emptyuser.text == "An Error Has Occurred!"


if __name__ == "__main__":
    main()
