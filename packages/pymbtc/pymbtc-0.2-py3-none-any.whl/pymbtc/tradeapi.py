# -*- coding: utf-8 -*-

import hashlib
import hmac
import time
from urllib.parse import urlencode

from . import base


class TradeApi(base.Base):
    """API de Negociações
    Documentação Oficial: 
    https://www.mercadobitcoin.com.br/trade-api/
    """

    def __init__(self, tapi_id, tapi_secret):
        super().__init__()
        self._tapi_id = tapi_id
        self._tapi_secret = tapi_secret
        self._path = "/tapi/v3/"

    def list_system_messages(self, level=None):
        """API Doc - List System Messages:
        https://www.mercadobitcoin.com.br/api-doc/#list_system_messages

        Método para comunicação de eventos do sistema relativos à TAPI, entre eles bugs, correções, manutenção programada e novas funcionalidades e versões. 
        
        O conteúdo muda a medida que os eventos ocorrem. 
        
        A comunicação externa, feita via Twitter e e-mail aos usuários da TAPI, continuará ocorrendo. 
        
        Entretanto, essa forma permite ao desenvolvedor tratar as informações juntamente ao seus logs ou até mesmo automatizar comportamentos.
        """

        res = self._post_request(
            tapi_method="list_system_messages",
            params={"level": level} if level is not None else {}
        )
        return res["messages"]

    def get_account_info(self):
        """API Doc - Get Account Info:
        https://www.mercadobitcoin.com.br/api-doc/#get_account_info

        Retorna dados da conta, como:
        1. saldos das moedas (Real, BCash, Bitcoin, Ethereum, Litecoin e XRP), 
        2. aldos considerando retenção em ordens abertas, 
        3. quantidades de ordens abertas por moeda digital, 
        4. limites de saque/transferências das moedas.
        """

        res = self._post_request(
            tapi_method="get_account_info",
        )
        return res

    def get_order(self, coin_pair, order_id):
        """API Doc - Get Order:
        https://www.mercadobitcoin.com.br/api-doc/#get_order

        Retorna os dados da ordem de acordo com o ID informado. 

        Dentre os dados estão as informações das Operações executadas dessa ordem. 

        Apenas ordens que pertencem ao proprietário da chave da TAPI pode ser consultadas. 
        
        Erros específicos são retornados para os casos onde o order_id informado não seja de uma ordem válida ou pertença a outro usuário.
        """

        res = self._post_request(
            tapi_method="get_order",
            params={"coin_pair": coin_pair, "order_id": order_id}
        )
        return res["order"]

    def list_orders(self, coin_pair, order_type=None, status_list=None, has_fills=None, from_id=None, to_id=None, from_timestamp=None, to_timestamp=None):
        """API Doc - List Orders:
        https://www.mercadobitcoin.com.br/api-doc/#list_orders

        Retorna uma lista de até 200 ordens, de acordo com os filtros informados, ordenadas pela data de última atualização. 
        
        As operações executadas de cada ordem também são retornadas. 
        
        Apenas ordens que pertencem ao proprietário da chave da TAPI são retornadas. 
        
        Caso nenhuma ordem seja encontrada, é retornada uma lista vazia.
        """

        res = self._post_request(
            tapi_method="list_orders",
            params={
                "coin_pair": coin_pair,
                "order_type": order_type,
                "status_list": order_type,
                "has_fills": order_type,
                "from_id": order_type,
                "to_id": order_type,
                "from_timestamp": order_type,
                "to_timestamp": order_type,
            }
        )
        return res["orders"]

    def list_orderbook(self, coin_pair, full=False):
        """API Doc - List Orderbook:
        https://www.mercadobitcoin.com.br/api-doc/#list_orderbook

        Retorna informações do livro de negociações (orderbook) do Mercado Bitcoin para o par de moedas (coin_pair) informado. 
        
        Diferente do método orderbook público descrito em /api-doc/#method_trade_api_orderbook, 
        
        aqui são fornecidas informações importantes para facilitar a tomada de ação de clientes TAPI e sincronia das chamadas. 
        
        Dentre elas, o número da última ordem contemplada (latest_order_id) e número das ordens do livro (order_id), descritos abaixo. 
        
        Importante salientar que nesse método ordens de mesmo preço não são agrupadas como feito no método público.
        """

        full = str(full).lower()
        res = self._post_request(
            tapi_method="list_orderbook",
            params={"coin_pair": coin_pair, "full": full}
        )
        return res["orderbook"]

    def place_buy_order(self, coin_pair, quantity, limit_price):
        """API Doc - Place Buy Order:
        https://www.mercadobitcoin.com.br/api-doc/#place_buy_order

        Abre uma ordem de compra (buy ou bid) do par de moedas, quantidade de moeda digital e preço unitário limite informados. 
        
        A criação contempla o processo de confrontamento da ordem com o livro de negociações. 
        
        Assim, a resposta pode informar se a ordem foi executada (parcialmente ou não) imediatamente após sua criação e, 
        
        assim, se segue ou não aberta e ativa no livro.
        """

        res = self._post_request(
            tapi_method="place_buy_order",
            params={
                "quantity": "{:.8f}".format(quantity),
                "limit_price": "{:.5f}".format(limit_price),
                "coin_pair": coin_pair
            }
        )
        return res["order"]

    def place_sell_order(self, coin_pair, quantity, limit_price):
        """API Doc - Place Sell Order:
        https://www.mercadobitcoin.com.br/api-doc/#place_sell_order

        Abre uma ordem de venda (sell ou ask) do par de moedas, quantidade de moeda digital e preço unitário limite informados. 
        
        A criação contempla o processo de confrontamento da ordem com o livro de negociações. 
        
        Assim, a resposta pode informar se a ordem foi executada (parcialmente ou não) imediatamente após sua criação e, 
        
        assim, se segue ou não aberta e ativa no livro.
        """

        res = self._post_request(
            tapi_method="place_sell_order",
            params={
                "quantity": "{:.8f}".format(quantity),
                "limit_price": "{:.5f}".format(limit_price),
                "coin_pair": coin_pair
            }
        )
        return res["order"]

    def place_market_buy_order(self, coin_pair, cost):
        """API Doc - Place Market Buy Order:
        https://www.mercadobitcoin.com.br/api-doc/#place_market_buy_order

        Abre uma ordem de compra (buy ou bid) do par de moedas com volume em reais limite informado. 
        
        A criação contempla o processo de bloqueio do saldo para execução da ordem e confrontamento da ordem com o livro de negociações. 
        
        Assim, a resposta pode informar se a ordem foi executada (parcialmente ou não) imediatamente após sua criação. 
        
        Caso não seja possível executá-la totalmente por restrições no saldo disponível do usuário, o montante não executado é cancelado.
        """

        res = self._post_request(
            tapi_method="place_market_buy_order",
            params={
                "cost": "{:.5f}".format(cost),
                "coin_pair": coin_pair
            }
        )
        return res["order"]

    def place_market_sell_order(self, coin_pair, quantity):
        """API Doc - Place Market Sell Order:
        https://www.mercadobitcoin.com.br/api-doc/#place_market_sell_order

        Abre uma ordem de venda (sell ou ask) do par de moeda com quantidade da moeda digital informado. 
        
        A criação contempla o processo de confrontamento da ordem com o livro de negociações. 
        
        Assim, a resposta pode informar se a ordem foi executada (parcialmente ou não) imediatamente após sua criação.
        """

        res = self._post_request(
            tapi_method="place_market_sell_order",
            params={
                "quantity": "{:.8f}".format(quantity),
                "coin_pair": coin_pair
            }
        )
        return res["order"]

    def cancel_order(self, coin_pair, order_id):
        """API Doc - Cancel Order:
        https://www.mercadobitcoin.com.br/api-doc/#cancel_order

        Cancela uma ordem, de venda ou compra, de acordo com o ID e par de moedas informado. 
        
        O retorno contempla o sucesso ou não do cancelamento, bem como os dados e status atuais da ordem. 
        
        Somente ordens pertencentes ao próprio usuário podem ser canceladas.
        """

        res = self._post_request(
            tapi_method="cancel_order",
            params={
                "coin_pair": coin_pair,
                "order_id": order_id
            }
        )
        return res["order"]

    def get_withdrawal(self, coin, withdrawal_id):
        """API Doc - Get Withdrawal:
        https://www.mercadobitcoin.com.br/api-doc/#get_withdrawal

        Retorna os dados de uma transferência de moeda digital ou de um saque de Real (BRL).
        """

        res = self._post_request(
            tapi_method="get_withdrawal",
            params={
                "coin": coin,
                "withdrawal_id": withdrawal_id
            }
        )
        return res["withdrawal"]

    def withdraw_coin_brl(self, quantity, account_ref, description=None):
        """API Doc - Withdraw Coin (BRL):
        https://www.mercadobitcoin.com.br/api-doc/#withdraw_coin

        Requisita pedido de transferência de moeda digital ou saque de Real. 
        
        Assim, caso o valor de coin seja BRL, então realiza um saque para a conta bancária informada. 
        
        Caso o valor seja uma criptomoeda, realiza uma transação para o endereço de moeda digital informado.
        """

        res = self._post_request(
            tapi_method="withdraw_coin",
            params={
                "coin": "BRL",
                "quantity": "{:.8f}".format(quantity),
                "account_ref": account_ref,
                "description": description,
            }
        )
        return res["withdrawal"]

    def withdraw_coin(self, coin, address, quantity, tx_fee, destination_tag=None, description=None):
        """API Doc - Withdraw Coin:
        https://www.mercadobitcoin.com.br/api-doc/#withdraw_coin

        Requisita pedido de transferência de moeda digital ou saque de Real. 
        
        Assim, caso o valor de coin seja BRL, então realiza um saque para a conta bancária informada. 
        
        Caso o valor seja uma criptomoeda, realiza uma transação para o endereço de moeda digital informado.
        """

        res = self._post_request(
            tapi_method="withdraw_coin",
            params={
                "coin": coin,
                "address": address,
                "quantity": "{:.8f}".format(quantity),
                "tx_fee": "{:.8f}".format(tx_fee),
                "destination_tag": destination_tag,
                "description": description,
            }
        )
        return res["withdrawal"]

    def _post_request(self, tapi_method, params={}):
        """https://www.mercadobitcoin.com.br/trade-api/#exemplo-completo-python
        """

        url_params = {
            'tapi_method': tapi_method,
            'tapi_nonce': str(int(time.time())),
        }
        url_params.update(params)
        filtered = {k: v for k, v in url_params.items() if v is not None}
        url_params.clear()
        url_params.update(filtered)

        # MAC
        params_string = self._path + '?' + urlencode(url_params)
        H = hmac.new(bytes(self._tapi_secret, encoding='utf8'),
                     digestmod=hashlib.sha512)
        H.update(params_string.encode('utf-8'))
        tapi_mac = H.hexdigest()

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'TAPI-ID': self._tapi_id,
            'TAPI-MAC': tapi_mac
        }

        res = super()._request(
            path=self._path,
            params=url_params,
            headers=headers,
            method="POST"
        )
        return res["response_data"]
