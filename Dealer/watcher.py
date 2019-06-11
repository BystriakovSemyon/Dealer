from itertools import permutations
from time import sleep
from datetime import datetime

from parsers import EXMOParser, CEXParser
from lib import Pair
from revenue import collect_deals
from settings import LOG, LOG_PATH


PARSERS_TO_RUN = [
    EXMOParser,
    CEXParser
]

PAIRS = [
    Pair('USD', 'BTC'),
    Pair('USD', 'ETH'),
    # Pair('USD', 'ZEC'),
]


def exchanges_orders_combiner(exchanges_order_books, pair):
    """
    Combine exchanges orders straight and vice versa.
    [(exch_1:sell, exch_2:buy), (exch_2:sell, exch_1:buy)]
    """
    for first_exchange, second_exchange in permutations(exchanges_order_books, 2):
        deals = []
        collect_deals(
            deals=deals,
            sell_exchange=first_exchange.exchange,
            buy_exchange=second_exchange.exchange,
            sell_orders=first_exchange.order_book.asks,
            buy_orders=second_exchange.order_book.bids,
            pair=pair
        )
        message = f'{datetime.now()} - Deals: {deals}'
        if deals:
            with open(f'{LOG_PATH}deals.txt', 'a') as f:
                f.write(message + '\n\n')
                print(message)

        with open(LOG, 'a') as f:
            f.write(f'{datetime.now()} - Deals: {list(map(str, deals))}\n')


def run():
    """Enter point."""
    for pair in PAIRS:
        exchanges_order_books = []
        for parser in PARSERS_TO_RUN:
            order_book = parser().get_order_book(pair)
            print(str(pair), parser.exchange.name)
            if order_book:
                exchanges_order_books.append(order_book)

        exchanges_orders_combiner(exchanges_order_books, pair)

        # Free endpoint doesn't allow us to make more that one rps
        sleep(1)


if __name__ == '__main__':
    print('start')
    while True:
        run()


# TODO: try to track more that one pair deal, for instance it can be usd/btc -> btc/eth | eth/btc -> btc/usd

# TODO: Add more exchanges, there are a lot of no fiat exchanges. - not worth time
