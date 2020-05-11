from watcher.lib import Fee, Unit, Exchange


CEX_IO = Exchange(
    name='cex.io',
    url='https://cex.io',
    fiat_fee={
        'USD': Fee(deposit=0.03, withdraw=0.03, unit=Unit.percentage),
        # 'USD': Fee(deposit=0, withdraw=0, unit=Unit.percentage),
    },
    coin_fee={
        'ZEC': Fee(deposit=0, withdraw=0.001, unit=Unit.value),
        'BTC': Fee(deposit=0, withdraw=0.0005, unit=Unit.value),
        'ETH': Fee(deposit=0, withdraw=0.01, unit=Unit.value),
    },
    trade_fee=0.0025,  # percentage
    # trade_fee=0,
    order_book_link='https://cex.io/api/order_book/{coin}/{fiat}/10',
)

EXMO = Exchange(
    name='exmo.me',
    url='https://exmo.me',
    fiat_fee={
        'USD': Fee(deposit=0.045, withdraw=0.0195, unit=Unit.percentage),
        # 'USD': Fee(deposit=0, withdraw=0, unit=Unit.percentage),
    },
    coin_fee={
        'ZEC': Fee(deposit=0, withdraw=0.001, unit=Unit.value),
        'BTC': Fee(deposit=0, withdraw=0.0004, unit=Unit.value),
        'ETH': Fee(deposit=0, withdraw=0.003, unit=Unit.value),
    },
    trade_fee=0.004,  # percentage
    # trade_fee=0,
    order_book_link='https://api.exmo.com/v1/order_book/?pair={coin}_{fiat}&limit=10',
)
