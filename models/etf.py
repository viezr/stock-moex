#!/usr/bin/env python3
"""
Model for moex etf
"""

import json
import xml.etree.ElementTree as ET
from models.base import Shares


class Etf(Shares):
    """
    Class for moex ETF shares attributes
    """
    market = "shares"
    board = "tqtf"
    def __init__(self, share_attrs=None):
        if share_attrs:
            super().__init__(share_attrs)

    @staticmethod
    def request_url(date):
        return str("http://iss.moex.com/iss/history/engines/stock/" +
                   f"markets/{Etf.market}/boards/{Etf.board}/" +
                   f"securities.json?date={date.isoformat()}")

    @staticmethod
    def convert_data(data, date):
        data = data.read().decode("utf-8")
        return data
