#!/usr/bin/env python3
"""
Module to get russian shares market and currency data
Data stored as dict in files "/data/*.json" for quick futher access
May be used without GUI.
"""
import os
import json
import socket
from urllib import request
import datetime as dt
import concurrent.futures
from config import cache_folder, export_file, shares_pool, currency_pool
from models.bonds import Bonds
from models.etf import Etf
from models.currency import Currency
from models.btc import Btc


def update_market_history(date):
    """
    Update market data for each type of share and currency
    """
    def request_market_history(date, share_class):
        """
        Request market data for given type of shares or currency from APIs.
        """
        file_name = f"data/{date.isoformat()}_{share_class.market}_{share_class.board}.json"
        if not os.path.isfile(file_name):
            request_url = share_class.request_url(date)
            try:
                data = request.urlopen(request_url)
            except:
                return False
            data = share_class.convert_data(data, date)
            if not write_file(data, file_name):
                return False
        return True

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future1 = executor.submit(request_market_history, date, Bonds())
        bonds = future1.result()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future2 = executor.submit(request_market_history, date, Etf())
        etf = future2.result()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future3 = executor.submit(request_market_history, date, Currency())
        currency = future3.result()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future4 = executor.submit(request_market_history, date, Btc())
        btc = future4.result()

    for fut in [future1, future2, future3, future4]:
        concurrent.futures.as_completed(fut)

    states = {"Bonds": bonds, "Etf": etf, "Currency": currency, "BTC": btc}
    info_str = " "
    for state in states:
        if not states[state]:
            info_str += f"{state} Fail. "
    return f"Updated{info_str}"


def get_shares_info(date, shares_request):
    """
    Request bunch of shares data from saved file and return to caller.
    """
    def get_share(date, share_class, share):
        """
        Request share data from saved file and return as share object
        """
        boards_classes = {"tqtf": Etf, "tqob": Bonds, "cbrf": Currency, "btc": Btc }

        file_name = f"{date.isoformat()}_{share_class.market}_{share_class.board}.json"
        if not os.path.exists(cache_folder):
            os.makedirs(cache_folder)
        if os.path.isfile(cache_folder + file_name):
            with open(cache_folder + file_name) as json_file:
                file_dict = json.load( json_file )["history"]["data"]
            for share_attrs in file_dict:
                if share in share_attrs[3]:
                    B_class = boards_classes[share_class.board]
                    return B_class(share_attrs)
        return None

    def share_thread(share):
        '''
        Thread for each share. Calls get_share
        '''
        Share_class = shares_classes[ share["type"].lower() ]
        share_card = get_share(date, Share_class(), share["name"])
        if share_card:
            return [share_card.market_name, share_card.market_index,
                    share_card.legal_close]
        else:
            return [share["name"], "Not found", 0]

    shares_classes = {"bonds": Bonds, "etf": Etf, "currency": Currency, "crypto": Btc}

    shares_out = {}
    for share in shares_request:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_share = executor.submit(share_thread, share)
            future_return = future_share.result()
        shares_out[share["name"]] = future_return
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

def write_file(data, file_name):
    """
    Saving requested data to file for futher using
    """
    if not data:
        return False
    data_json = json.loads( data )["history.cursor"]["data"][0]
    if data_json[1] > 0:
        with open(file_name, mode="w", encoding="utf-8") as file:
            file.write(data)
        return True
    else:
        return False



if __name__ == "__main__":
    """
    For console run
    """
    if check_internet():
        source_date = dt.date(2021, 9, 9)
        print("Update market:", update_market_history(source_date))
        one_share = [ { "type": "bonds",
                        "name": "26233",
                        "buy_date": "None",
                        "price": 0 } ]

        print(get_shares_info(source_date, one_share))
