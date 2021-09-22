"""
Config
"""
cache_folder = "data/"

# Used only for GUI menu
shares_types = ["common", "bonds", "etf", "currency", "crypto"]

# For export simple data (name;price) to link with office documents
export_file = "/home/this/Documents/market_rates.txt"

# In shares_pool stored bougth shares, as portfolio and for export
shares_pool = [
    { "type": "bonds",
      "name": "SU26224",
      "buy_date": "2021-07-14",
      "price": 90.177 },
    { "type": "bonds",
      "name": "SU26238",
      "buy_date": "2021-07-14",
      "price": 92.1 },
    { "type": "etf",
      "name": "FXCN",
      "buy_date": "2021-07-14",
      "price": 3200 },
    { "type": "etf",
      "name": "VTBX",
      "buy": "2021-07-14",
      "price": 139.8 },
    { "type": "common",
      "name": "SBER",
      "buy": "2021-07-14",
      "price": 310.42 }
 ]

# In currency_pool stored request for GUI bottom info and for export
currency_pool = [
    { "type": "currency",
      "name": "USD",
      "buy_date": "None",
      "price": 0 },
    { "type": "currency",
      "name": "EUR",
      "buy_date": "None",
      "price": 0 },
    { "type": "crypto",
      "name": "BTC",
      "buy_date": "None",
      "price": 0 },
 ]
