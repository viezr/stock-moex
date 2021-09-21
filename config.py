"""
Config

In shares_pool stored bougth shares
In currency_pool stored request for main window bottom info
export_file used for export simple data (name;price) to link with office documents
"""
cache_folder = "data/"

shares_types = ["bonds", "etf", "currency", "crypto"]

export_file = "/home/this/Documents/market_rates.txt"

shares_pool = [
    { "type": "bonds",
      "name": "SU26233",
      "buy_date": "2021-05-13",
      "price": 90.177 },
    { "type": "bonds",
      "name": "SU26235",
      "buy_date": "2021-05-14",
      "price": 92.1 },
    { "type": "etf",
      "name": "FXUS",
      "buy_date": "2021-05-14",
      "price": 5588 },
    { "type": "etf",
      "name": "VTBX",
      "buy": "2021-05-17",
      "price": 139.8 },
    { "type": "etf",
      "name": "FXCN",
      "buy": "2021-05-17",
      "price": 3820 }
 ]

currency_pool = [
    { "type": "currency",
      "name": "USD",
      "buy_date": "None",
      "price": 0 },
    { "type": "currency",
      "name": "EUR",
      "buy_date": "None",
      "price": 0
    },
    { "type": "crypto",
      "name": "BTC",
      "buy_date": "None",
      "price": 0 },
 ]
