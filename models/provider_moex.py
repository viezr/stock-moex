'''
Provider module for moex bonds
'''
from .provider import Provider


class ProviderMoex(Provider):
    '''
    Class for moex bonds provider
    '''
    def request_url(self, date: object) -> str:
        '''
        Request url subclass dependend.
        '''
        date_req = date.isoformat()
        url = str("http://iss.moex.com/iss/history/engines/stock/" +
                  f"markets/{self.market}/boards/{self.board}/" +
                  f"securities.json?date={date_req}")
        return url

    def convert_data(self, data: object, date: object = None) -> str:
        '''
        Change data structure to common format.
        '''
        data = data.read().decode("utf-8")
        return data
