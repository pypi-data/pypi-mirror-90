from rich import print
from cryt.client import Client


class Order(object):
    def __init__(self, client: Client):
        self.__client = client
        self.lo = _LimitOrder(client)


class _LimitOrder(object):
    def __init__(self, client: Client):
        self.__client = client

    def sell(self, size: float, price_depth: float):
        price = self.__client.get_ticker()["ask"] + price_depth
        print(self.__client.create_limit_order("sell", price, size))

    def buy(self, size: float, price_depth: float):
        price = self.__client.get_ticker()["bid"] - price_depth
        print(self.__client.create_limit_order("buy", price, size))
