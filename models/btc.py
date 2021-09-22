#!/usr/bin/env python3
"""
Model for BTC
"""
import json
from models.base_model import Shares


class Btc(Shares):
    """
    Class for BTC attributes
    """
    market = "crypto"
    board = "btc"
    provider = "coindesk"

    def __init__(self, share_attrs=None):
        if share_attrs:
            super().__init__(share_attrs)

    def convert_data(data, date):
        '''
        Change data structure to common format
        '''
        data = data.read().decode("ascii")
        if "bpi" in data:
            data_json = json.loads(data)["bpi"]
            dict_json = {"history":{"data": []}, "history.cursor":{"data": []}}
            items_count = 0
            if str(date.isoformat()) in data_json:
                for item in data_json:
                    dict_json["history"]["data"].append(
                        [Btc.board, date.isoformat(), "BTC-USD", "BTCUSD",
                         0,0,0,0,0, data_json[item]])
                    items_count += 1
            dict_json["history.cursor"]["data"].append([0,items_count,100])
            data = json.dumps(dict_json, ensure_ascii=False, indent=4)
        return data

    def request_url(cls, date):
        """
        Request url
        """
        url = str("https://api.coindesk.com/v1/bpi/historical/close.json?" +
                  f"start={date.isoformat()}&end={date.isoformat()}")
        return url
