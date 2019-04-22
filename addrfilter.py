import re
from enum import Enum
from itertools import zip_longest
from bitcoinaddressvalidator import check_bc
from bitcoinbech32addressvalidator import bech32_verify_checksum
from eth_utils import is_address


__all__ = [
    "BITCOIN", "ETHEREUM", "BITCOIN_CASH", "LITECOIN",
    "DOGECOIN", "DASH", "BITCOIN_SV", "BINANCE_COIN", "MAKER",
    "MONERO", "EOS", "findalladdresses"
]

_BITCOIN_REGEX = r'(?<=\b)[13][1-9A-HJ-NP-Za-km-z]{25,34}'
_BITCOIN_BECH32_REGEX = r'(?<=\b)bc1[02-9ac-hj-np-z]{6,87}'
_ETHEREUM_REGEX = r'(?<=\b)0x[0-9a-fA-F]{40}'
_BITCOIN_CASH_REGEX = r'(?<=\b)([qp][02-9ac-hj-np-z]{60,104}|[qp][02-9AC-HJ-NP-Z]{60,104})'  # Legacy addresses are the same as Bitcoin, Lower case is preferred for cashaddr, but uppercase is accepted. A mixture of lower case and uppercase must be rejected.
_LITECOIN_REGEX = r'(?<=\b)[ML][1-9A-HJ-NP-Za-km-z]{25,34}'
_LITECOIN_BECH32_REGEX = r'(?<=\b)ltc1[02-9ac-hj-np-z]{6,86}'
_DOGECOIN_REGEX = r'(?<=\b)D[1-9A-HJ-NP-Za-km-z]{25,34}'  # Dogecoin addresses regex is the same as DeepOnion addresses regex
_DASH_REGEX = r'(?<=\b)X[1-9A-HJ-NP-Za-km-z]{25,34}'
_BITCOIN_SV_REGEX = r'(?<=\b)([qp][02-9ac-hj-np-z]{60,104}|[qp][02-9AC-HJ-NP-Z]{60,104})'  # equal to Bitcoin Cash
_BINANCE_COIN_REGEX = r'(?<=\b)0x[0-9a-fA-F]{40}'  # same as Ethereum address
_MAKER_REGEX = r'(?<=\b)0x[0-9a-fA-F]{40}'  # same as Ethereum address
_MONERO_REGEX = r'(?<=\b)4[1-9A-HJ-NP-Za-km-z]{94}'
_EOS_REGEX = r'(?<=\b)0x[0-9a-fA-F]{40}'  # same as Ethereum address

res = [
    ([re.compile(_BITCOIN_REGEX), re.compile(_BITCOIN_BECH32_REGEX)], "Bitcoin address"),
    (re.compile(_ETHEREUM_REGEX), "Ethereum address"),
    (re.compile(_BITCOIN_CASH_REGEX), "BitcoinCash address"),
    ([re.compile(_LITECOIN_REGEX), re.compile(_LITECOIN_BECH32_REGEX)], "Litecoin address"),
    (re.compile(_DOGECOIN_REGEX), "Dogecoin address"),
    (re.compile(_DASH_REGEX), "Dash address"),
    (re.compile(_BITCOIN_SV_REGEX), "BitcoinSV address"),
    (re.compile(_BINANCE_COIN_REGEX), "BinanceCoin address"),
    (re.compile(_MAKER_REGEX), "Maker address"),
    (re.compile(_MONERO_REGEX), "Monero address"),
    (re.compile(_EOS_REGEX), "EOS address")
]

validators = [
    [check_bc, bech32_verify_checksum],
    is_address
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
    validator = validators[address_type.value]

    return extractaddress(s, regex, validator)


def findalladdresses(s):
    useraddrs = set()
    for regex, validator in zip_longest(res, validators):
        useraddrs.update(extractaddress(s, regex, validator))

    return useraddrs


def extractaddress(s, regex, validator):
    newuseraddrs = set()
    addrs = []

    if type(regex[0]) == list:
        for reg in regex[0]:
            addrs.extend(reg.findall(s))
    else:
        addrs = regex[0].findall(s)

    for addr in addrs:
        if addr:
            newuseraddrs.add((regex[1], addr))

    # Check if the addresses are valid with respective validators
    if newuseraddrs and validator:
        _newuseraddrs = newuseraddrs.copy()
        for addr in _newuseraddrs:
            addr = addr[1]
            if type(regex[0]) == list:
                for r, v in zip_longest(regex[0], validator):
                    if r.match(addr):
                        if not v(addr):
                            newuseraddrs.remove((regex[1], addr))
            else:
                if not validator(addr):
                    newuseraddrs.remove((regex[1], addr))

    return newuseraddrs
