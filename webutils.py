from urllib.request import urlopen, Request


def gethtml(url):
    #  Bitcoin Talk wants User-Agent to work properly
    req = Request(url=url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/70.0.3538.77 Safari/537.36'})
    resource = urlopen(req)

    content = resource.read().decode(resource.headers.get_content_charset())
    resource.close()

    return content
