#!/usr/bin/env python3
"""
Base model for common moex shares attributes
"""

class Shares():
    """
    Class for common moex shares attributes
    """
    def __init__(self, share_attrs=None):
        if share_attrs:
            self.boardid = share_attrs[0]
            self.date = share_attrs[1]
            self.market_name = share_attrs[2]
            self.market_index = share_attrs[3]
            self.legal_close = share_attrs[9]
