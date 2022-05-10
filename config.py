"""
Config
"""
cache_folder = "data/"

# For export simple data (name;price) to link with office documents
export_file = "/home/this/market_rates.txt"

boards = [
    {"name": "Bonds", "board": "tqob", "market": "bonds", "provider_name": "moex"},
    {"name": "ETF","board": "tqtf", "market": "shares", "provider_name": "moex"},
    {"name": "Common", "board": "tqbr", "market": "shares", "provider_name": "moex"},
    {"name": "Currency RU", "board": "cbr", "market": "currency", "provider_name": "cbr"},
    {"name": "Currency GE", "board": "nbg", "market": "currency", "provider_name": "nbg"},
    {"name": "BTCUSD", "board": "btc", "market": "crypto", "provider_name": "coindesk"},
    {"name": "Crypto", "board": "binance", "market": "crypto", "provider_name": "binance"}
]

# In shares_pool stored bougth shares, as portfolio
# showed at GUI startup
shares_pool = [
    {
        "board": "tqob",
        "name": "SU26224",
        "buy_date": "2021-07-14",
        "price": 90.177
    },
    {
        "board": "tqtf",
        "name": "SBER",
        "buy": "2021-07-14",
        "price": 310.42
    },
    {
        "board": "tqtf",
        "name": "VTBX",
        "buy_date": "2021-05-17",
        "price": 139.8
    },
    {
        "board": "tqtf",
        "name": "FXCN",
        "buy_date": "2021-05-17",
        "price": 3820
    }
 ]

# List of currencies for GUI bottom info
currency_pool = [
      {"board": "cbr", "name": "USDRUB"},
      {"board": "nbg", "name": "EURRUB"},
      {"board": "btc", "name": "BTCUSD"}
 ]

# List for exporting prices to file
export_pool = [
    {"board": "tqtf", "name": "VTBX"},
    {"board": "tqtf", "name": "FXCN"},
    {"board": "cbr", "name": "USDRUB"},
    {"board": "cbr", "name": "EURRUB"},
    {"board": "btc", "name": "BTCUSD"},
    {"board": "binance", "name": "BTCUSDT"},
]
