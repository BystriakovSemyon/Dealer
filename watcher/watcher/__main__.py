from watcher.log_helpers import setup_logger

from itertools import permutations
from time import sleep

from watcher.parsers import EXMOParser, CEXParser
from watcher.lib import Pair
from watcher.revenue import collect_deals


PARSERS_TO_RUN = [
    EXMOParser,
    CEXParser
]

PAIRS = [
    Pair('USD', 'BTC'),
    Pair('USD', 'ETH'),
    # Pair('USD', 'ZEC'),
]


def exchanges_orders_combiner(exchanges_order_books, pair, logger):
    """
    Combine exchanges orders straight and vice versa.
    [(exch_1:sell, exch_2:buy), (exch_2:sell, exch_1:buy)]
    """
    for first_exchange, second_exchange in permutations(exchanges_order_books, 2):
        collect_deals(
            sell_exchange=first_exchange.exchange,
            buy_exchange=second_exchange.exchange,
            sell_orders=first_exchange.order_book.asks,
            buy_orders=second_exchange.order_book.bids,
            pair=pair,
            logger=logger
        )


def run(logger):
    """Enter point."""
    for pair in PAIRS:
        exchanges_order_books = []
        for parser in PARSERS_TO_RUN:
            order_book = parser().get_order_book(pair)
            print(str(pair), parser.exchange.name)
            if order_book:
                exchanges_order_books.append(order_book)

        exchanges_orders_combiner(exchanges_order_books, pair, logger)

        # Free endpoint doesn't allow us to make more that one rps
        sleep(1)


# TODO: add web front application
# TODO: try to track more that one pair deal, for instance it can be usd/btc -> btc/eth | eth/btc -> btc/usd


# TODO: Add more exchanges, there are a lot of no fiat exchanges. - not worth time


if __name__ == '__main__':
    logger = setup_logger('WatcherRootLogger')
    logger.info('Start')
    try:
        while True:
            logger.debug('Heart beat')
            run(logger)
    except:
        logger.exception('Fail!')
    finally:
        logger.info('End')
