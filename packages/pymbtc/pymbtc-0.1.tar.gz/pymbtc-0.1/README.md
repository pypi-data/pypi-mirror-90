## Mercado Bitcoin - API de Dados e Negociações

* * *

### Documentação Oficial

+ [API de Dados](https://www.mercadobitcoin.com.br/api-doc/)
    - [ticker](https://www.mercadobitcoin.com.br/api-doc/#method_trade_api_ticker)
    - [orderbook](https://www.mercadobitcoin.com.br/api-doc/#method_trade_api_orderbook)
    - [trades](https://www.mercadobitcoin.com.br/api-doc/#method_trade_api_trades)
    - [day_summary](https://www.mercadobitcoin.com.br/api-doc/#method_trade_api_daysummary)


+ [API de Negociações](https://www.mercadobitcoin.com.br/trade-api/)
    - [list_system_messages](https://www.mercadobitcoin.com.br/trade-api/#list_system_messages)
    - [get_account_info](https://www.mercadobitcoin.com.br/trade-api/#get_account_info)
    - [get_order](https://www.mercadobitcoin.com.br/trade-api/#get_order)
    - [list_orders](https://www.mercadobitcoin.com.br/trade-api/#list_orders)
    - [list_orderbook](https://www.mercadobitcoin.com.br/trade-api/#list_orderbook)
    - [place_buy_order](https://www.mercadobitcoin.com.br/trade-api/#place_buy_order)
    - [place_sell_order](https://www.mercadobitcoin.com.br/trade-api/#place_sell_order)
    - [place_market_buy_order](https://www.mercadobitcoin.com.br/trade-api/#place_market_buy_order)
    - [place_market_sell_order](https://www.mercadobitcoin.com.br/trade-api/#place_market_sell_order)
    - [cancel_order](https://www.mercadobitcoin.com.br/trade-api/#cancel_order)
    - [get_withdrawal](https://www.mercadobitcoin.com.br/trade-api/#get_withdrawal)
    - [withdraw_coin](https://www.mercadobitcoin.com.br/trade-api/#withdraw_coin)

* * *

### Exemplo de Uso
    from pymbtc import Api, TradeApi
    import os
    
    api = Api()
    print(api.ticker())
    print(api.ticker("BTC"))
    
    tapi = TradeApi(
        tapi_id=os.getenv("tapi_id"),
        tapi_secret=os.getenv("tapi_secret")
    )
    print(tapi.list_system_messages())
    print(tapi.list_system_messages(level="INFO"))
    print(tapi.get_account_info())
    print(tapi.list_orders(coin_pair="BRLBTC"))