from collections import namedtuple
from enum import Enum


class Unit(Enum):
    percentage = 'P'
    value = 'V'


Fee = namedtuple('Fee', 'deposit, withdraw, unit')
Deal = namedtuple('Deal', 'sell_order, buy_order, gain, pair, sell_exchange, buy_exchange')
Deal.__str__ = (
    lambda self, *args, **kwargs:
    f'gain: {self.gain} {self.pair.fiat}, exchanges: {self.sell_exchange}, {self.buy_exchange}'
)

Exchange = namedtuple(
    'Exchange', 'name, url, fiat_fee, coin_fee, trade_fee, order_book_link')

ExchangeOrderBook = namedtuple('ExchangeRawOrders', 'exchange, order_book, pair')

OrderBook = namedtuple('OrderBook', 'asks, bids')

Order = namedtuple('Order', 'price, value')

ExchangesOrdersCombination = namedtuple(
    'ExchangesOrdersCombination', 'sell_exchange, buy_exchange, sell_orders, buy_orders')

Pair = namedtuple('Pair', 'fiat, coin')
