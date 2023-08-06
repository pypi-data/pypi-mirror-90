# -*- coding: utf-8 -*-

from datetime import datetime

from . import base


class Api(base.Base):
    """API de Dados
    Documentação Oficial:
    https://www.mercadobitcoin.com.br/api-doc/
    """

    def __init__(self, default_coin="BTC"):
        super().__init__()
        self.default_coin = default_coin

    def ticker(self, coin="BTC"):
        """API Doc: https://www.mercadobitcoin.com.br/api-doc/#method_trade_api_ticker

        Retorna informações com o resumo das últimas 24 horas de negociações.
        """
        res = super()._request(
            path=f"/api/{coin}/ticker"
        )
        return res["ticker"]

    def orderbook(self, coin="BTC"):
        """API Doc: https://www.mercadobitcoin.com.br/api-doc/#method_trade_api_orderbook

        Livro de ofertas é composto por duas listas:
        1. uma lista com as ofertas de compras ordenadas pelo maior valor
        2. uma lista com as ofertas de venda ordenadas pelo menor valor

        O livro mostra até 1000 ofertas de compra e até 1000 ofertas de venda.

        Uma oferta é constituída por uma ou mais ordens.

        A quantidade da oferta é a soma das quantidades das ordens de mesmo preço unitário.

        Caso uma oferta represente mais de uma ordem, a prioridade de execução se dá com base na data de criação da ordem, da mais antiga para a mais nova.
        """
        res = super()._request(
            path=f"/api/{coin}/orderbook"
        )
        return res

    def trades(self, coin="BTC"):
        """API Doc: https://www.mercadobitcoin.com.br/api-doc/#method_trade_api_trades

        Histórico de negociações realizadas.
        """
        res = super()._request(
            path=f"/api/{coin}/trades"
        )
        return res

    def day_summary(self, date=datetime.today(), coin="BTC"):
        """API Doc: https://www.mercadobitcoin.com.br/api-doc/#method_trade_api_daysummary

        Retorna resumo diário de negociações realizadas.

        Exemplo:
        --------
        day_summary(datetime(2014, 6, 25))
        """
        res = super()._request(
            path=f"/api/{coin}/day-summary/{date.year}/{date.month}/{date.day}"
        )
        return res
