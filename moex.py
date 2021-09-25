#!/usr/bin/env python3
"""
Module to get russian shares market and currency data
Data stored as dict in files "/data/*.json" for quick futher access
May be used without GUI.
"""
import os
import json
import socket
import datetime as dt
import concurrent.futures
from config import cache_folder, export_file, shares_pool, currency_pool
from models.common import Common
from models.bonds import Bonds
from models.etf import Etf
from models.currency import Currency
from models.btc import Btc
from models.utils import request_data


def update_market_history(date):
    """
    Update market data for each type of share and currency
    """
    states = {}
    futures = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for class_name, Share_class in shares_classes.items():
            future_update = executor.submit(request_data, Share_class, date)
            states[Share_class.__name__] = future_update.result
    concurrent.futures.as_completed(future_update)

    info_str = " "
    for state in states:
        if not states[state]():
            info_str += f"{state} Fail. "
    return f"Updated{info_str}"


def get_shares_info(date, shares_request):
    """
    Request bunch of shares data from saved file and return to caller.
    """
    def get_share(date, Share_class, share_name):
        """
        Request share data from saved file and return as share object
        """
        file_name = f"{date.isoformat()}_{Share_class.market}_{Share_class.board}.json"
        if os.path.isfile(cache_folder + file_name):
            with open(cache_folder + file_name) as json_file:
                file_dict = json.load( json_file )["history"]["data"]
            for share_attrs in file_dict:
                if share_name.lower() in share_attrs[3].lower():
                    return Share_class(share_attrs)
        return None

    def share_thread(share):
        '''
        Thread for each share. Calls get_share
        '''
        Share_class = shares_classes[ share["type"].lower() ]
        share_card = get_share(date, Share_class, share["name"])
        if share_card:
            return [share_card.market_name, share_card.market_index,
                    share_card.legal_close]
        else:
            return [share["name"], "Not found", 0]

    if not os.path.exists(cache_folder):
        os.makedirs(cache_folder)

    shares_out = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for share in shares_request:
            future_share = executor.submit(share_thread, share)
            future_return = future_share.result
            shares_out[share["name"]] = future_return()
    concurrent.futures.as_completed(future_share)

    return shares_out

def export_data(date):
    """
    Export data for shares in config.py to a file (path in config.py),
    in simple format "name;price" for link to office document
    """
    shares_dict = get_shares_info(date, shares_pool)
    shares_dict.update(get_shares_info(date, currency_pool))
    if not shares_dict:
        return False

    with open(export_file, "w") as file:
        data = "Date;" + str(date.strftime("%d/%m/%Y"))
        for share in shares_dict:
            data += "\n" + str(shares_dict[share][1]) + ";" + str(shares_dict[share][2])
        file.write(data)
    return True

def check_internet():
    for timeout in [1,5,10,15]:
        try:
            socket.setdefaulttimeout(timeout)
            host = socket.gethostbyname("www.google.com")
            s = socket.create_connection((host, 80), 2)
            s.close()
            return True
        except:
            pass
    return False


shares_classes = {"common": Common, "bonds": Bonds, "etf": Etf, "currency": Currency, "crypto": Btc}

if __name__ == "__main__":
    """
    For console run
    """
    if check_internet():
        source_date = dt.date(2021, 9, 24)
        print(source_date)
        print("Request:", shares_pool)
        print("Update market:", update_market_history(source_date))
        print("Answer:", get_shares_info(source_date, shares_pool))
