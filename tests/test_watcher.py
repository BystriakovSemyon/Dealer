from unittest.mock import Mock, mock_open, call, patch

from lib import Pair
import watcher


def test_exchanges_orders_combiner(mocker):
    exchanges_order_book_1 = Mock()
    exchanges_order_book_1.exchange = 'test first exchange'
    exchanges_order_book_1.order_book.asks = 'test first order_book asks'
    exchanges_order_book_1.order_book.bids = 'test first order_book bids'
    exchanges_order_book_2 = Mock()
    exchanges_order_book_2.exchange = 'test second exchange'
    exchanges_order_book_2.order_book.asks = 'test second order_book asks'
    exchanges_order_book_2.order_book.bids = 'test second order_book bids'

    exchanges_order_books = [exchanges_order_book_1, exchanges_order_book_2]
    collect_deals_mock = mocker.patch('watcher.collect_deals')
    pair = Pair('TST', 'TST')

    with patch('builtins.open', mock_open()) as mock_file:
        watcher.exchanges_orders_combiner(exchanges_order_books, pair)

    collect_deals_mock.assert_has_calls([
        call(
            deals=[],
            sell_exchange='test first exchange',
            buy_exchange='test second exchange',
            sell_orders='test first order_book asks',
            buy_orders='test second order_book bids',
            pair=pair
        ),
        call(
            deals=[],
            sell_exchange='test second exchange',
            buy_exchange='test first exchange',
            sell_orders='test second order_book asks',
            buy_orders='test first order_book bids',
            pair=pair
        ),
    ])


def test_run(mocker):
    parser_to_run_1 = Mock()
    parser_to_run_1.return_value.get_order_book.return_value = 'test order_book 1'
    parser_to_run_2 = Mock()
    parser_to_run_2.return_value.get_order_book.return_value = None

    watcher.PARSERS_TO_RUN = [parser_to_run_1, parser_to_run_2]
    test_pair = Pair('TST', 'TST')
    watcher.PAIRS = [test_pair]
    mocker.patch('watcher.sleep')

    exchanges_orders_combiner_mock = mocker.patch('watcher.exchanges_orders_combiner')

    watcher.run()
    exchanges_orders_combiner_mock.assert_called_with(['test order_book 1'], test_pair)

    parser_to_run_1.return_value.get_order_book.assert_called_with(test_pair)
    parser_to_run_2.return_value.get_order_book.assert_called_with(test_pair)

