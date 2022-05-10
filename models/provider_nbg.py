'''
Provider module for Georgian currency
'''
import json

from .provider import Provider


class ProviderNbg(Provider):
    '''
    Class for Georgian currency provider
    '''
    def request_url(self, date: object) -> str:
        '''
        Request url.
        '''
        date_req = date.strftime("%Y-%m-%d")
        url = str("https://nbg.gov.ge/gw/api/ct/monetarypolicy/" +
            f"currencies/en/json/?date={date_req}")
        return url

    def convert_data(self, data: object, date: object = None) -> str:
        '''
        Change data structure to common format
        '''
        di = json.load(data)
        currencies = di[0]["currencies"]

        dict_json = {"history":{"data": []}, "history.cursor":{"data": []}}
        items_count = 0
        for cur in currencies:
            code = cur["code"] + "GEL"
            rate = cur["rate"] / cur["quantity"]
            dict_json["history"]["data"].append([
                self.board, date.isoformat(), cur["name"], code,
                0,0,0,0,0, rate])
            items_count += 1
        if items_count == 0:
            return None
        dict_json["history.cursor"]["data"].append([0, items_count, 100])
        data = json.dumps(dict_json, ensure_ascii=False, indent=4)

        return data
