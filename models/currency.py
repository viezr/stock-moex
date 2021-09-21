#!/usr/bin/env python3
"""
Model for currency
"""

import json
import xml.etree.ElementTree as ET
from models.base import Shares


class Currency(Shares):
    """
    Class for currency attributes
    """
    market = "currency"
    board = "cbrf"
    def __init__(self, share_attrs=None):
        if share_attrs:
            super().__init__(share_attrs)

    @staticmethod
    def request_url(date):
        date_req = date.strftime("%d/%m/%Y")
        return str(f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={date_req}")

    @staticmethod
    def convert_data(data, date):
        '''
        Change data structure to common format
        '''
        data = data.read().decode("cp1251")
        root = ET.fromstring(data)
        dict_json = {"history":{"data": []}, "history.cursor":{"data": []}}
        items_count = 0
        if "ValCurs" in data:
            for item in root.findall("./Valute"):
                dict_json["history"]["data"].append([
                    Currency.board, date.isoformat(), item[3].text, item[1].text,
                    0,0,0,0,0, float(item[4].text.replace(",","."))
                ])
                items_count += 1
        dict_json["history.cursor"]["data"].append([0, items_count, 100])
        data = json.dumps(dict_json, ensure_ascii=False, indent=4)

        return data
