#!/usr/bin/env python3
'''
Module to get russian shares market and currency data
Data stored as dict in files "/data/*.json" for quick futher access
May be used without GUI.
'''
import os
import json
import socket
import datetime as dt
import concurrent.futures

from config import cache_folder, export_file, shares_pool, export_pool, boards
from models import BoardFactory, Share


def update_market_history(date):
    '''
    Update market data for each type of share and currency
    '''
    states = {}
    board_factory = BoardFactory()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for board_attrs in boards:
            board = board_factory.get_board(**board_attrs)
            future_update = executor.submit(board.request_data, date)
            states[board.board] = future_update.result
    concurrent.futures.as_completed(future_update)

    info_str = " "
    for board, result in states.items():
        if not result():
            info_str += f"{board} Fail. "
    return f"Updated{info_str}"


def get_shares_info(date, shares_request):
    '''
    Request bunch of shares data from saved file and return to caller.
    '''
    shares_out = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for share in shares_request:
            future_share = executor.submit(_share_thread, date, share)
            future_return = future_share.result
            shares_out[share["name"]] = future_return()
    concurrent.futures.as_completed(future_share)

    return shares_out

def _share_thread(date: object, share: dict) -> list:
    '''
    Thread for each share. Calls _get_share
    '''
    share_card = _get_share(date, share)
    if share_card:
        return [share_card.market_name, share_card.market_index,
                share_card.legal_close]
    return [share["name"], "Not found", 0]

def _get_share(date: object, share: dict) -> [object, None]:
    '''
    Request share data from saved file and return as share object
    '''
    file_path = _get_share_file_path(date, share["board"])
    if os.path.isfile(file_path):
        with open(file_path) as json_file:
            file_dict = json.load( json_file )["history"]["data"]
        for share_file in file_dict:
            if share["name"].lower() in share_file[3].lower():
                return Share(share_file)
    return None

def _get_share_file_path(date: object, board_name: str) -> str:
    board_attrs = [x for x in boards if x["board"] == board_name][0]
    board_factory = BoardFactory()
    board = board_factory.get_board(**board_attrs)
    file_path = board.get_file_path(date)
    return file_path

def export_data(date):
    '''
    Export data for shares in config.py to a file (path in config.py),
    in simple format "name;price" for link to office document
    '''
    shares_dict = get_shares_info(date, shares_pool)
    shares_dict.update(get_shares_info(date, export_pool))
    if not shares_dict:
        return False

    with open(export_file, "w") as file:
        data = "Date;" + str(date.strftime("%d/%m/%Y"))
        for share in shares_dict.values():
            share_name, share_price = share[1:3]
            data += "\n" + share_name + ";" + str(share_price)
        file.write(data)
    return True

def check_internet():
    '''
    Check internet.
    '''
    for timeout in [1,5,10,15]:
        try:
            socket.setdefaulttimeout(timeout)
            host = socket.gethostbyname("www.google.com")
            soc = socket.create_connection((host, 80), 2)
            soc.close()
            return True
        except:
            pass
    return False

def console_run(source_date):
    '''
    Run app without GUI.
    '''
    if not os.path.exists(cache_folder):
        os.makedirs(cache_folder)

    if not check_internet():
        return
    print(source_date)
    print("Update market:", update_market_history(source_date))
    shares = get_shares_info(source_date, shares_pool)
    for key, val in shares.items():
        for req_share in shares_pool:
            if req_share["name"] == key:
                price = req_share["price"]
                change = round(((val[2] / price * 100) - 100), 2)
        print(f"{key:<10} Current {val[2]:>8}\tBuy {price:>8} " +
            f"\tChange {change:>7} %")
    export_data(source_date)


if __name__ == "__main__":
    #source_date = dt.date(2022, 5, 6)
    source_date = dt.date.today()
    console_run(source_date)
