#!/usr/bin/env python3
"""
Model for moex etf
"""
from models.base_model import Shares


class Etf(Shares):
    """
    Class for moex ETF shares attributes
    """
    market = "shares"
    board = "tqtf"
    provider = "moex"

    def __init__(self, share_attrs=None):
        if share_attrs:
            super().__init__(share_attrs)

    def convert_data(data, date):
        data = data.read().decode("utf-8")
        return data

    def request_url(cls, date):
        """
        Request url
        """
        url = str("http://iss.moex.com/iss/history/engines/stock/" +
                  f"markets/{cls.market}/boards/{cls.board}/" +
                  f"securities.json?date={date.isoformat()}")
        return url
