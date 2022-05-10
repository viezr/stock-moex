'''
Base provider module
'''
import os
import json
from urllib import request
from config import cache_folder


class Provider():
    '''
    Base class for provider
    '''
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

    def request_url(self, date: object) -> str:
        '''
        Request url. Subclass responsibility
        '''
        err = ' '.join([self.__class__.__name__, "doesn't support this method"])
        raise NotImplementedError(err)

    def convert_data(self, data: object, date: object = None) -> str:
        '''
        Change data structure to common format
        '''
        err = ' '.join([self.__class__.__name__, "doesn't support this method"])
        raise NotImplementedError(err)

    def request_data(self, date):
        '''
        Request market data for given type of shares or currency from APIs.
        '''
        request_url = self.request_url(date)
        file_path = self.get_file_path(date)

        data = None
        if not os.path.isfile(file_path):
            #try:
            data = request.urlopen(request_url)
            data = self.convert_data(data, date)
            #except:
            #    return False
            if self.provider_name == "moex":
                data = self.combine_pages(data, request_url)
            if data:
                self.save_file(data, file_path)
        return True

    def save_file(self, data: str, file_path: str):
        with open(file_path, mode="w", encoding="utf-8") as f:
            f.write(data)

    def combine_pages(self, data, request_url):
        '''
        Moex answers paginated. If answer has more than 100 shares,
        function request other pages and combine them
        '''
        combined_data = json.loads( data )
        pages_info = combined_data["history.cursor"]["data"][0]
        shares_start = pages_info[0]
        shares_total = pages_info[1]
        shares_per_page = pages_info[2]

        if shares_total == 0:
            return None
        if shares_total <= shares_per_page:
            return data

        pages = shares_total // shares_per_page + 1
        for page in range(1, pages):
            shares_start = shares_per_page + shares_start + 1
            new_request_url = f"{request_url}&start={shares_start}"
            new_data = request.urlopen(new_request_url)
            new_data = self.convert_data(new_data, None)
            new_data = json.loads( new_data )

        for item in new_data["history"]["data"]:
           combined_data["history"]["data"].append(item)

        combined_data["history.cursor"]["data"][0][2] = shares_total
        data = json.dumps(combined_data, indent=4)
        return data

    def get_file_path(self, date):
        file_path = ''.join([cache_folder, date.isoformat(), "_",
            self.market, "_", self.board, "_", self.provider_name, ".json"])
        return file_path
