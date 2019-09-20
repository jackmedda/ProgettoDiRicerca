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
import re
from enum import Enum
from itertools import zip_longest
from bitcoinaddressvalidator import check_bc
from bitcoinbech32addressvalidator import bech32_verify
from eth_utils import is_address
import copy


__all__ = [
    "BITCOIN", "ETHEREUM", "BITCOIN_CASH", "LITECOIN",
    "DOGECOIN", "DASH", "BITCOIN_SV", "MONERO",
    "findalladdresses", "findaddressesbytype"
]

_BITCOIN_REGEX = r'(?<=\b)[13][1-9A-HJ-NP-Za-km-z]{25,34}'
_BITCOIN_BECH32_REGEX = r'(?<=\b)bc1[02-9ac-hj-np-z]{6,87}'
_ETHEREUM_REGEX = r'(?<=\b)0x[0-9a-fA-F]{40}'
_BITCOIN_CASH_REGEX = r'(?<=\b)([qp][02-9ac-hj-np-z]{60,104}|[qp][02-9AC-HJ-NP-Z]{60,104})'  # Legacy addresses are the same as Bitcoin, Lower case is preferred for cashaddr, but uppercase is accepted. A mixture of lower case and uppercase must be rejected.
_LITECOIN_REGEX = r'(?<=\b)[ML][1-9A-HJ-NP-Za-km-z]{25,34}'  # also addresses starting with 3, same as Bitcoin
_LITECOIN_BECH32_REGEX = r'(?<=\b)ltc1[02-9ac-hj-np-z]{6,86}'
_DOGECOIN_REGEX = r'(?<=\b)D[1-9A-HJ-NP-Za-km-z]{25,34}'  # Dogecoin addresses regex is the same as DeepOnion addresses regex
_DASH_REGEX = r'(?<=\b)X[1-9A-HJ-NP-Za-km-z]{25,34}'
_BITCOIN_SV_REGEX = r'(?<=\b)([qp][02-9ac-hj-np-z]{60,104}|[qp][02-9AC-HJ-NP-Z]{60,104})'  # equal to Bitcoin Cash
_MONERO_REGEX = r'(?<=\b)4[1-9A-HJ-NP-Za-km-z]{94}'

# Array of compiled regexs
res = [
    ([re.compile(_BITCOIN_REGEX), re.compile(_BITCOIN_BECH32_REGEX)], "Bitcoin address"),
    (re.compile(_ETHEREUM_REGEX), "Ethereum address"),
    (re.compile(_BITCOIN_CASH_REGEX), "BitcoinCash address"),
    ([re.compile(_LITECOIN_REGEX), re.compile(_LITECOIN_BECH32_REGEX)], "Litecoin address"),
    (re.compile(_DOGECOIN_REGEX), "Dogecoin address"),
    (re.compile(_DASH_REGEX), "Dash address"),
    (re.compile(_BITCOIN_SV_REGEX), "BitcoinSV address"),
    (re.compile(_MONERO_REGEX), "Monero address")
]

# Array of checksum validator
validators = {
    "Bitcoin address": [check_bc, bech32_verify],
    "Ethereum address": is_address
}


class _Address(Enum):
    """Contains the enumeration for mapping each value with a certain regex"""
    BITCOIN = 0
    ETHEREUM = 1
    BITCOIN_CASH = 2
    LITECOIN = 3
    DOGECOIN = 4
    DASH = 5
    BITCOIN_SV = 6
    MONERO = 7
globals().update(_Address.__members__)


def findaddressesbytype(s, address_type):
    """
    Find all addresses of the type given as parameter
    :param s: string from which addresses are extracted
    :param address_type: type of address to be extracted. Types are in class _Address
    :return: a set of tuples (Crypto Name, address)
    """
    regex = res[address_type.value]

    return _extractaddress(s, regex)


def findalladdresses(s):
    """
    Find all addresses using the regexs of crypto in the array "res"
    :param s: string from which addresses are extracted
    :return: a set of tuples (Crypto Name, address)
    """
    useraddrs = set()
    for regex in res:
        useraddrs.update(_extractaddress(s, regex))

    return useraddrs


def _extractaddress(s, regex):
    """
    Extract addresses from a string using the regex passed as parameter
    :param s: string from which addresses are extracted
    :param regex: regular expression for a given crypto
    :return: a set of tuples (Crypto Name, address)
    """
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

    if newuseraddrs:
        _newuseraddrs = copy.deepcopy(newuseraddrs)
        for addr in _newuseraddrs:
            if addr[0] in validators:
                validator = validators[addr[0]]
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
