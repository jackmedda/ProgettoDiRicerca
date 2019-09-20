from urllib.request import urlopen, Request
from json import load
from os import stat


def gethtml(url):
    """
    Function to get the html of a page given a url with the right charset
    :param url: url (string) of the page
    :return: html of the page
    """
    #  Bitcoin Talk wants User-Agent to work properly
    req = Request(url=url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/70.0.3538.77 Safari/537.36'})
    resource = urlopen(req)

    content = resource.read().decode(resource.headers.get_content_charset())
    resource.close()

    return content


# Actually works just for BitcoinTalk
def load_data(filepath, offset):
    """
    Load data from the json of BitcoinTalkUsers.json
    Before it worked also for crawl Blockchain.com, but it was needed to be modified because of some modifications
    to BitcoinTalk crawling work. Anyway Blockchain.com crawling and scraping is a fast process
    :param filepath:
    :param offset: the pages work by means of an integer offset (e.g. user_id --> +1, page_results --> +50)
    :return: loaded data and index from which position the code restart
    """
    data = []
    startindex = 0
    try:
        jsonfile = open(filepath, 'r')
        # Loads the json file and takes last key of the loaded dictionary
        if jsonfile:
            if stat(jsonfile.name).st_size != 0:
                data = load(jsonfile)
                startindex = int(data[-1]["BitcoinTalkID"]) + offset
                # startindex = int(list(data.keys())[-1]) + offset
                if "Name" not in data[-1]:
                    del data[-1]

        jsonfile.close()
    except IOError:
        pass

    return data, startindex


def tupleset_to_dict_of_sets(addresses):
    """
    Helper function first used to get a dictionary of sets from the tuple set returned by the functions
    for finding addresses of addrfilter.py file
    :param addresses: set of tuples with each entry as (Crypto Name, address)
    :return: a dictionary of sets
    """
    result = {}
    for x in addresses:
        if x[0] in result:
            result[x[0]].add(x[1])
        else:
            result[x[0]] = {x[1]}

    for r in result:
        result[r] = list(result[r])

    return result
