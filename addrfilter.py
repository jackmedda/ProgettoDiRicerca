import re
from enum import Enum

str1 = "Like my answer? Did I help? Tips gratefully accepted here: 1H6wM8Xj8GNrhqWBrnDugd8Vf3nAfZgMnq"

str2 = "amiller on freenode / 19G6VFcV1qZJxe3Swn28xz3F8gDKTznwEM"

str3 = "3862 West Fork Drive Plantation, FL 33324" # NO

str4 = "plus size black dresses (http://www.swakdesigns.com/c-134-black-dresses.aspx)" # NO

str5 = "Philips norelco 1280cc combining gyroflex 3d, ultratrack heads and skinglide, results in an extremely close shave in fewer strokes." # NO

str6 = "3139" # NO

str7 = "plus size black dresses (http://www.swakdesigns.com/c-134-black-dresses.aspx) 1H6wM8Xj8GNrhqWBrnDugd8Vf3nAfZgMnq"

strings = (str1, str2, str3, str4, str5, str6, str7)


__all__ = [
    "BITCOIN"
]


# _bitcoinre = [re.compile(r'1[1-9A-HJ-NP-Za-km-z]{25,34}$'), re.compile(r'3[1-9A-HJ-NP-Za-km-z]{25,34}$'), re.compile(r'(?=bc1)[1-9A-HJ-NP-Za-km-z]{25,34}$')]
_bitcoinre = re.compile(r'1[1-9A-HJ-NP-Za-km-z]{25,34}$')

class _Address(Enum):
    BITCOIN = 1
    ETHEREUM = 2

globals().update(_Address.__members__)


def findstraddresses(address_type):
    if address_type == _Address.BITCOIN:
        regexs = _bitcoinre

        for s in strings:
            #for regex in regexs:
                print(s)
                print(regexs.findall(s))

findstraddresses(_Address.BITCOIN)