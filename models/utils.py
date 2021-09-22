#!/usr/bin/env python3
"""
Models utils
"""
import os
import json
from urllib import request
from config import cache_folder


def combine_pages(cls, data, request_url):
    '''
    Moex answers paginated. If answer has more than 100 shares,
    function request other pages and combine them
    '''
    combined_data = json.loads( data )
    pages_info = combined_data["history.cursor"]["data"][0]
    shares_start = pages_info[0]
    shares_total = pages_info[1]
    shares_per_page = pages_info[2]

    if shares_total > shares_per_page:
        pages = shares_total // shares_per_page + 1

        for page in range(1, pages):
            shares_start = shares_per_page + shares_start + 1
            new_request_url = f"{request_url}&start={shares_start}"
            new_data = request.urlopen(new_request_url)
            new_data = cls.convert_data(new_data, None)
            new_data = json.loads( new_data )

            for item in new_data["history"]["data"]:
                combined_data["history"]["data"].append(item)
        combined_data["history.cursor"]["data"][0][2] = shares_total
        data = json.dumps(combined_data, indent=4)
    return data

def request_data(cls, date):
    """
    Request market data for given type of shares or currency from APIs.
    """
    request_url = cls.request_url(cls, date)
    file = f"{cache_folder}{date.isoformat()}_{cls.market}_{cls.board}.json"
    data = None

    if not os.path.isfile(file):
        try:
            data = request.urlopen(request_url)
            data = cls.convert_data(data, date)
        except:
            return False
        if cls.provider == "moex":
            data = combine_pages(cls, data, request_url)
        with open(file, mode="w", encoding="utf-8") as f:
            f.write(data)
    return True
