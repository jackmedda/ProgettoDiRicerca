import re
from enum import Enum


__all__ = [
    "BITCOIN", "ETHEREUM", "BITCOIN_CASH", "LITECOIN",
    "DOGECOIN", "DASH", "BITCOIN_SV", "BINANCE_COIN", "MAKER"
]

_BITCOIN_REGEX = r'(?<=\W)[13][1-9A-HJ-NP-Za-km-z]{25,34}'
_BITCOIN_BECH32_REGEX = r'(?<=\W)bc1[02-9ac-hj-np-z]{6,87}'
_ETHEREUM_REGEX = r'(?<=\W)0x[0-9a-fA-F]{40}'
_BITCOIN_CASH_REGEX = r'(?<=\W)'
_LITECOIN_REGEX = r'(?<=\W)'
_DOGECOIN_REGEX = r'(?<=\W)'
_DASH_REGEX = r'(?<=\W)'
_BITCOIN_SV_REGEX = r'(?<=\W)'
_BINANCE_COIN_REGEX = r'(?<=\W)'
_MAKER_REGEX = r'(?<=\W)'

res = [
    ([re.compile(_BITCOIN_REGEX), re.compile(_BITCOIN_BECH32_REGEX)], "Bitcoin address"),
    (re.compile(_ETHEREUM_REGEX), "Ethereum address"),
    (re.compile(_BITCOIN_CASH_REGEX), "BitcoinCash address"),
    (re.compile(_LITECOIN_REGEX), "Litecoin address"),
    (re.compile(_DOGECOIN_REGEX), "Dogecoin address"),
    (re.compile(_DASH_REGEX), "Dash address"),
    (re.compile(_BITCOIN_SV_REGEX), "BitcoinSV address"),
    (re.compile(_BINANCE_COIN_REGEX), "BinanceCoin address"),
    (re.compile(_MAKER_REGEX), "Maker address")
]


class _Address(Enum):
    BITCOIN = 0
    ETHEREUM = 1
    BITCOIN_CASH = 2
    LITECOIN = 3
    DOGECOIN = 4
    DASH = 5
    BITCOIN_SV = 6
    BINANCE_COIN = 7
    MAKER = 8

globals().update(_Address.__members__)


def findaddressesbytype(s, address_type):
    regex = res[address_type.value]

    print(extractaddress(regex, s))
    return extractaddress(regex, s)


def findalladdresses(s):
    useraddrs = set()
    for regex in res:
        useraddrs.update(extractaddress(regex, s))

    print(useraddrs)
    return useraddrs


def extractaddress(regex, s):
    useraddrs = set()
    addrs = []

    if type(regex[0]) == list:
        for reg in regex[0]:
            addrs.extend(reg.findall(s))
    else:
        addrs = regex[0].findall(s)

    for addr in addrs:
        if addr:
            useraddrs.add((regex[1], addr))
    return useraddrs

# TEST

str1 = "Like my answer? Did I help? Tips 19G6VFcV1qZJxe3Swn28xz3F8gDKTznwEM gratefully accepted here: 1H6wM8Xj8GNrhqWBrnDugd8Vf3nAfZgMnq"

str2 = "amiller on freenode / 19G6VFcV1qZJxe3Swn28xz3F8gDKTznwEM"

str3 = "3862 West Fork 0x9Ca0e998dF92c5351cEcbBb6Dba82Ac2266f7e0C Drive Plantation, FL 33324" # NO

str4 = "plus size black dresses (http://www.swakdesigns.com/c-134-black-dresses.aspx)" # NO

str5 = "Philips norelco 1280cc combining gyroflex 3d, ultratrack heads and skinglide, results in an extremely close shave in fewer strokes." # NO

str6 = "3139" # NO

str7 = "plus size 0xCd2a3d9f938e13Cd947eC05ABC7fe734df8DD826 black bc1qwqdg6squsna38e46795at95yu9atm8azzmyvckulcc7kytlcckxswvvzej dresses (http://www.swakdesigns.com/c-134-black-dresses.aspx) -1H6wM8Xj8GNrhqWBrnDugd8Vf3nAfZgMnq"

strings = (str1, str2, str3, str4, str5, str6, str7)

findalladdresses(str7)
findaddressesbytype(str7, _Address.BITCOIN)

findaddressesbytype(str3, _Address.ETHEREUM)
