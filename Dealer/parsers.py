from datetime import datetime

import requests

from exchanges import CEX_IO, EXMO
from lib import Order, OrderBook, ExchangeOrderBook
from settings import LOG_PATH, LOG


class Parser:
    exchange = None

    def collect_orders(self, raw_orders):
        return [Order(float(order[0]), float(order[1])) for order in raw_orders]

    def order_book_link_maker(self, pair):
        return self.exchange.order_book_link.format(coin=pair.coin, fiat=pair.fiat)

    def parse_order_book(self, response, pair):
        response = response.json()
        return OrderBook(
            asks=self.collect_orders(response['asks']),
            bids=self.collect_orders(response['bids'])
        )

    def get_order_book(self, pair):
        request = self.order_book_link_maker(pair)
        response = requests.get(request)
        message = '{} - Request: {}\nResponse: {}\n'.format(datetime.now(), request, response.text)
        # with open(f'{LOG_PATH}{self.exchange.name}.txt', 'a') as f:
        #     f.write(message)

        try:
            exchange_order_book = ExchangeOrderBook(
                exchange=self.exchange,
                order_book=self.parse_order_book(response, pair),
                pair=pair
            )
        except KeyError:
            self.error_handler(request, response, message)
            exchange_order_book = None

        return exchange_order_book

    def error_handler(self, request, response, message):
        try:
            if response.json().get('error') == 'Rate limit exceeded':
                with open(LOG, 'a') as f:
                    f.write(f'RATE LIMIT EXCEEDED: {request}\n')
            else:
                with open(f'{LOG_PATH}bad_response.txt', 'a') as f:
                    f.write(message)

        except Exception:
            # If response is not a json
            with open(f'{LOG_PATH}bad_response.txt', 'a') as f:
                f.write(message)


class CEXParser(Parser):
    exchange = CEX_IO
    pass


class EXMOParser(Parser):
    exchange = EXMO

    def parse_order_book(self, response, pair):
        response = response.json()
        pair_str = f'{pair.coin}_{pair.fiat}'
        return OrderBook(
            asks=self.collect_orders(response[pair_str]['ask']),
            bids=self.collect_orders(response[pair_str]['bid'])
        )
