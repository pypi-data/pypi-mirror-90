from __future__ import annotations
import abc
import os
from dataclasses import dataclass

import ccxt
from ccxt.base.exchange import Exchange


class Client(metaclass=abc.ABCMeta):
    def __init__(self, symbol: str, exchange: Exchange):
        self.symbol = symbol
        self.exchange = exchange

    @classmethod
    def __get_bitflyer(cls, symbol: str) -> Exchange:
        access_key = os.environ.get("CRYT_BITFLYER_KEY")
        access_secret = os.environ.get("CRYT_BITFLYER_SECRET")

        bitflyer = ccxt.bitflyer(
            {
                "apiKey": access_key,
                "secret": access_secret,
            }
        )
        return _BitflyerClient(symbol, bitflyer)

    @classmethod
    def create(cls, exchange_name: str, symbol: str) -> Client:
        return {"bitflyer": cls.__get_bitflyer}[exchange_name](symbol)

    @abc.abstractmethod
    def get_positions(self):
        pass

    def get_orders(self):
        return self.exchange.fetch_open_orders(symbol=self.symbol)

    def get_ticker(self):
        return self.exchange.fetch_ticker(self.symbol)

    def cancel_order(self, order_id: str):
        self.exchange.cancel_order(order_id, symbol=self.symbol)


    def create_limit_order(self, side: str, price: float, size: float):
        if side == "buy":
            return self.exchange.create_limit_buy_order("FX_BTC_JPY", size, price)
        elif side == "sell":
            return self.exchange.create_limit_sell_order("FX_BTC_JPY", size, price)
        else:
            raise ValueError()


class _BitflyerClient(Client):
    def __init__(self, symbol: str, exchange: Exchange):
        super().__init__(symbol, exchange)

    def get_positions(self):
        return self.exchange.private_get_getpositions(
            params={"product_code": self.symbol}
        )
