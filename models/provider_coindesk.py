'''
Provider module for BTC
'''
import json
import datetime as dt

from .provider import Provider


class ProviderCoindesk(Provider):
    '''
    Class for BTC provider
    '''
    def request_url(self, date: object) -> str:
        '''
        Request url
        '''
        if date == dt.date.today():
            url = "https://api.coindesk.com/v1/bpi/currentprice.json"
        else:
            url = str("https://api.coindesk.com/v1/bpi/historical/close.json?" +
                f"start={date.isoformat()}&end={date.isoformat()}")
        return url

    def convert_data(self, data: object, date: object) -> str:
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
                        [self.board, date.isoformat(), "BTC-USD", "BTCUSD",
                         0,0,0,0,0, data_json[item]])
                    items_count += 1
            elif "USD" in data_json:
                dict_json["history"]["data"].append(
                    [self.board, date.isoformat(), "BTC-USD", "BTCUSD",
                     0,0,0,0,0, data_json["USD"]["rate_float"]])
                items_count += 1

            if items_count == 0:
                return None
            dict_json["history.cursor"]["data"].append([0,items_count,100])
            data = json.dumps(dict_json, ensure_ascii=False, indent=4)
        return data
