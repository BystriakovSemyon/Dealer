
from watcher.lib import Order, Pair, Fee
from watcher import revenue


def test_calculate_gain_no_gain():
    sell_order = Order(10, 0.11)
    buy_order = Order(10, 0.2)
    assert revenue.calculate_gain(None, None, sell_order, buy_order, None) == 0


def test_calculate_gain(mocker):
    sell_exchange = mocker.Mock()
    sell_exchange.fiat_fee = {'TST': Fee(0.0001, 0.0002, 'test')}
    sell_exchange.coin_fee = {'TST': Fee(0.0003, 0.0004, 'test')}
    sell_exchange.trade_fee = 0.001

    buy_exchange = mocker.Mock()
    buy_exchange.fiat_fee = {'TST': Fee(0.0005, 0.0006, 'test')}
    buy_exchange.coin_fee = {'TST': Fee(0.0007, 0.0008, 'test')}
    buy_exchange.trade_fee = 0.002

    sell_order = Order(10, 0.1)
    buy_order = Order(12, 0.2)
    pair = Pair('TST', 'TST')

    assert revenue.calculate_gain(sell_exchange, buy_exchange, sell_order, buy_order, pair) == 0.18338


def test_collect_deals(mocker):
    deals = []
    sell_exchange = mocker.Mock()
    sell_exchange.name = 'test sell_exchange'
    buy_exchange = mocker.Mock()
    buy_exchange.name = 'test buy_exchange'

    sell_orders = ['test sell_orders 1', 'test sell_orders 2']
    buy_orders = ['test buy_orders 1', 'test buy_orders 2']
    pair = 'test pair'

    calculate_gain = mocker.Mock()
    calculate_gain.side_effect = [1, 0]
    revenue.calculate_gain = calculate_gain

    revenue.collect_deals(deals, sell_exchange, buy_exchange, sell_orders, buy_orders, pair)
    assert deals == [revenue.Deal(
        sell_order='test sell_orders 1',
        buy_order='test buy_orders 1',
        gain=1,
        pair='test pair',
        sell_exchange='test sell_exchange',
        buy_exchange='test buy_exchange'
    )]
