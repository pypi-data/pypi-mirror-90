from __future__ import annotations
from rich import print
from cryt.client import Client

class Cancel(object):
    def __init__(self, client: Client):
        self.__client = client

    def all_orders(self):
        orders = self.__client.get_orders()
        for order in orders:
            print(self.__client.cancel_order(order['id']))
