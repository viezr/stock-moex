#!/usr/bin/env python3
"""
Model for moex bonds
"""
from models.base_model import Shares

class Bonds(Shares):
    """
    Class for moex bonds shares attributes
    """
    market = "bonds"
    board = "tqob"
    provider = "moex"

    def __init__(self, share_attrs=None):
        if share_attrs:
            super().__init__(share_attrs)
            self.nkd = share_attrs[10]
            self.percent = share_attrs[26]
            self.nominal = share_attrs[30]

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
