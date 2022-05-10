'''
Provider module for Russian currency
'''
import json
import xml.etree.ElementTree as ET

from .provider import Provider


class ProviderCbr(Provider):
    '''
    Class for currency Russian provider
    '''
    def request_url(self, date: object) -> str:
        '''
        Request url.
        '''
        date_req = date.strftime("%d/%m/%Y")
        url = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={date_req}"
        return url

    def convert_data(self, data: object, date: object = None) -> str:
        '''
        Change data structure to common format
        '''
        data = data.read().decode("cp1251")
        root = ET.fromstring(data)
        dict_json = {"history":{"data": []}, "history.cursor":{"data": []}}
        items_count = 0
        if "ValCurs" in data:
            for item in root.findall("./Valute"):
                code = item[1].text + "RUB"
                dict_json["history"]["data"].append([
                    self.board, date.isoformat(), item[3].text, code,
                    0,0,0,0,0, float(item[4].text.replace(",","."))
                ])
                items_count += 1
        if items_count == 0:
            return None
        dict_json["history.cursor"]["data"].append([0, items_count, 100])
        data = json.dumps(dict_json, ensure_ascii=False, indent=4)

        return data
