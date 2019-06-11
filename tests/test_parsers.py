from unittest.mock import patch, mock_open, call

from lib import Pair
import parsers


def test_collect_orders():
    raw_orders = [('0', '1'), ('0.0', '1.1'), (.1, 1)]
    assert parsers.Parser().collect_orders(raw_orders) == [(0, 1), (0, 1.1), (.1, 1)]


def test_order_book_link_maker(mocker):
    parsers.Parser.exchange = mocker.Mock()
    parsers.Parser.exchange.order_book_link = 'coin={coin}, fiat={fiat}'
    assert parsers.Parser().order_book_link_maker(Pair('FAT', 'CIN')) == 'coin=CIN, fiat=FAT'


def test_parse_order_book(mocker):
    parsers.Parser.collect_orders = lambda self, arg: arg
    response = mocker.Mock()
    response.json.return_value = {
        'asks': 'test asks',
        'bids': 'test bids'
    }
    assert parsers.Parser().parse_order_book(response, None) == \
        parsers.OrderBook(asks='test asks', bids='test bids')


def test_get_order_book(mocker):
    parser = parsers.Parser()

    exchange = mocker.Mock()
    exchange.name = 'test exchange name'
    parser.exchange = exchange

    order_book_link_maker_mock = mocker.Mock()
    order_book_link_maker_mock.return_value = 'test request'
    parser.order_book_link_maker = order_book_link_maker_mock

    response_mock = mocker.Mock()
    response_mock.text = 'test text response'
    get_mock = mocker.patch('parsers.requests.get')
    get_mock.return_value = response_mock

    datetime = mocker.patch('parsers.datetime')
    datetime.now.return_value = 'NOW'

    parse_order_book = mocker.patch('parsers.Parser.parse_order_book')
    parse_order_book.return_value = 'test order_book'

    error_handler_mock = mocker.Mock()
    parser.error_handler = error_handler_mock

    test_pair = Pair('TST', 'TST')

    with patch('builtins.open', mock_open()) as mock_file:
        order_book = parser.get_order_book(test_pair)

        assert order_book == parsers.ExchangeOrderBook(
            exchange=exchange,
            order_book='test order_book',
            pair=test_pair
        )
        mock_file().write.assert_called_once_with(
            'NOW - Request: test request\nResponse: test text response\n')

        parse_order_book.assert_called_with(response_mock, test_pair)

        order_book_link_maker_mock.assert_called_with(test_pair)
        get_mock.assert_called_with('test request')
        error_handler_mock.assert_not_called()


def test_get_order_book_key_error(mocker):
    parser = parsers.Parser()

    parser.exchange = mocker.Mock()
    order_book_link_maker_mock = mocker.Mock()
    order_book_link_maker_mock.return_value = 'test request'
    parser.order_book_link_maker = order_book_link_maker_mock

    response_mock = mocker.Mock()
    response_mock.text = 'test text response'
    get_mock = mocker.patch('parsers.requests.get')
    get_mock.return_value = response_mock

    datetime = mocker.patch('parsers.datetime')
    datetime.now.return_value = 'NOW'

    error_handler_mock = mocker.Mock()
    parser.error_handler = error_handler_mock

    mocker.patch('parsers.Parser.parse_order_book', side_effect=KeyError)

    with patch('builtins.open', mock_open()):
        assert parser.get_order_book(Pair('TST', 'TST')) is None

        error_handler_mock.assert_called_with(
            'test request',
            get_mock(),
            'NOW - Request: test request\nResponse: test text response\n'
        )


def test_error_handler(mocker):
    parser = parsers.Parser()

    request = 'test request'
    response = mocker.Mock()
    response.json.return_value = {'error': 'Rate limit exceeded'}
    message = 'test message'

    with patch('builtins.open', mock_open()) as mock_file:
        parser.error_handler(request, response, message)

        mock_file().write.assert_called_once_with(
            f'RATE LIMIT EXCEEDED: test request\n')
        mock_file.assert_has_calls([call('log/log.txt', 'a')])


def test_error_handler_unknown_error(mocker):
    parser = parsers.Parser()

    request = 'test request'
    response = mocker.Mock()
    response.json.return_value = {'error': 'unknown_error'}
    message = 'test message'

    with patch('builtins.open', mock_open()) as mock_file:
        parser.error_handler(request, response, message)

        mock_file().write.assert_called_once_with('test message')
        mock_file.assert_has_calls([call('log/bad_response.txt', 'a')])


def test_error_handler_exception(mocker):
    parser = parsers.Parser()

    request = 'test request'
    response = mocker.Mock()
    response.json.side_effect = Exception
    message = 'test message'

    with patch('builtins.open', mock_open()) as mock_file:
        parser.error_handler(request, response, message)

        mock_file().write.assert_called_once_with('test message')
        mock_file.assert_has_calls([call('log/bad_response.txt', 'a')])


def test_EXMOParser_parse_order_book(mocker):
    response = mocker.Mock()
    response.json.return_value = {
        'TST2_TST1': {
            'ask': 'test asks',
            'bid': 'test bids',
        }
    }
    assert parsers.EXMOParser().parse_order_book(response, Pair('TST1', 'TST2')) == \
        parsers.OrderBook(asks='test asks', bids='test bids')


