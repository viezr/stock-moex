#!/usr/bin/env python3
"""
Base model for common moex shares attributes
"""


class Share():
    """
    Class for common moex shares attributes
    """
    def __init__(self, share_attrs: list):
        if share_attrs:
            self.boardid = share_attrs[0]
            self.date = share_attrs[1]
            self.market_name = share_attrs[2]
            self.market_index = share_attrs[3]
            self.legal_close = share_attrs[9]
            self.nkd = share_attrs[10] if len(share_attrs) > 10 else None
            self.percent = share_attrs[26] if len(share_attrs) > 26 else None
            self.nominal = share_attrs[30] if len(share_attrs) > 30 else None
