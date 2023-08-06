# -*- coding: utf-8 -*-

import json
import time
from datetime import datetime
from http import client
from urllib.parse import urlencode


class Base:
    """Classe base para se comunicar com a API do Mercado Bitcoin
    """

    def __init__(self):
        """Taxa limite de requisições:
        https://www.mercadobitcoin.com.br/trade-api/#taxa-limite-de-requisi%C3%A7%C3%B5es
        """
        self.delay_s = 1.5
        self.t_1 = datetime.now()
        self.host = "www.mercadobitcoin.net"

    def _sleep(self):
        now = datetime.now()
        elapsed = (now - self.t_1).total_seconds()
        if elapsed < self.delay_s:
            time.sleep(self.delay_s - elapsed)

    def _request(self, path="/", method="GET", params=None, headers=None):
        self._sleep()
        if params is None:
            params = {}
        if headers is None:
            headers = {}
        params = urlencode(params)
        result = None
        try:
            conn = client.HTTPSConnection(self.host)
            conn.request(method.upper(), path, params, headers)
            response = conn.getresponse()
            response = response.read()
            response_json = json.loads(response)
            result = response_json
        finally:
            if conn:
                conn.close()
                self.t_1 = datetime.now()
        return result
