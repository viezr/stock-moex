'''
Provider module for BTC
'''
import json
import datetime as dt

from .provider import Provider


class ProviderBinance(Provider):
    '''
    Class for BTC Binance provider
    '''
    def request_url(self, date) -> str:
        '''
        Request url
        '''
        url = "https://api.binance.com/api/v3/ticker/price"
        return url

    def convert_data(self, data: object, date: object) -> str:
        '''
        Change data structure to common format
        '''
        data = data.read().decode("ascii")

        data_json = json.loads(data)
        dict_json = {"history":{"data": []}, "history.cursor":{"data": []}}
        items_count = 0
        if date == dt.date.today():
            for item in data_json:
                item_name = '-'.join([item["symbol"][:3], item["symbol"][3:]])
                dict_json["history"]["data"].append(
                    [self.board, date.isoformat(), item_name, item["symbol"],
                     0,0,0,0,0, item["price"]])
                items_count += 1
        if items_count == 0:
            return None
        dict_json["history.cursor"]["data"].append([0,items_count,100])
        data = json.dumps(dict_json, ensure_ascii=False, indent=4)
        return data
