
def calculate_gain(sell_exchange, buy_exchange, sell_order, buy_order, pair):
    """
    Check if there is a 'positive' price difference between two exchanges.
    Add all fees to be more accurate.
    """
    price_difference = buy_order.price - sell_order.price

    if price_difference > 0:
        min_value = round(min(buy_order.value, sell_order.value), 5)

        # We are buying 'good' sell order and sell to close 'good' buy order
        my_buy_order = sell_order.price * min_value
        my_sell_order = buy_order.price * min_value

        # We need to balance our exchanges deposits after all deals, so we calculate fees keeping that in mind.

        # fiat fees always are percentage
        fiat_fees = (sell_exchange.fiat_fee[pair.fiat].deposit * my_buy_order +
                     buy_exchange.fiat_fee[pair.fiat].withdraw * my_sell_order)

        # per transaction(fee is a constant value)
        coin_fees = (sell_exchange.coin_fee[pair.coin].withdraw * sell_order.price +
                     buy_exchange.coin_fee[pair.coin].deposit * buy_order.price)

        trade_fees = my_buy_order * sell_exchange.trade_fee + my_sell_order * buy_exchange.trade_fee

        gain = round((my_sell_order - my_buy_order) - fiat_fees - coin_fees - trade_fees, 8)
    else:
        gain = 0

    return gain


def collect_deals(sell_exchange, buy_exchange, sell_orders, buy_orders, pair, logger):
    """
    Looking for a good deals and stop when gain is equal to zero.
    Orders are sorted by price increase, so zipping them is fine for the beginning.
    """
    # todo: we need decision maker instead of zip
    for sell_order, buy_order in zip(sell_orders, buy_orders):
        gain = calculate_gain(sell_exchange, buy_exchange, sell_order, buy_order, pair)
        if gain <= 0:
            break

        deal = {
            'sell_order': sell_order,
            'buy_order': buy_order,
            'gain': gain,
            'pair': pair,
            'sell_exchange': sell_exchange.name,
            'buy_exchange': buy_exchange.name
        }
        logger.info('Deal', extra={'deal': deal})
