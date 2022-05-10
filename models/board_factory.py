'''
Shares providers factory module
'''
from .provider_moex import ProviderMoex
from .provider_cbr import ProviderCbr
from .provider_nbg import ProviderNbg
from .provider_coindesk import ProviderCoindesk
from .provider_binance import ProviderBinance


class BoardFactory():
    '''
    Shares provider factory class.
    '''
    providers = {
        "moex": ProviderMoex,
        "cbr": ProviderCbr,
        "nbg": ProviderNbg,
        "binance": ProviderBinance,
        "coindesk": ProviderCoindesk
    }

    @classmethod
    def get_board(cls, **kwargs) -> object:
        '''
        Return provider instance.
        '''
        provider_name = kwargs["provider_name"]
        board = cls.providers[provider_name](**kwargs)
        return board
