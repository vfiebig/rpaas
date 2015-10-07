# -*- coding: utf-8 -*-
from rpaas.ssl_plugins import BaseSSLPlugin
import requests
import base64
import os
import urllib
# from lxml import html


class InvalidToken(Exception):
    pass

class GloboDomains(BaseSSLPlugin):

    def __init__(self, id=None):
        self.base_url = os.getenv('RPAAS_PLUGIN_GLOBODOMAINS_URL', None)
        self.client_id = os.getenv('RPAAS_PLUGIN_GLOBODOMAINS_ID', None)
        self.client_secret = os.getenv('RPAAS_PLUGIN_GLOBODOMAINS_SECRET', None)
        self.oauth_url = os.getenv('RPAAS_PLUGIN_GLOBODOMAINS_BSURL', None)
        self.id = id
        self._bearer = self._get_token()
        self._domainid = None

    def _get_token(self):
        try:
            resp = requests.post(self.oauth_url, 
                data={
                    'grant_type':'client_credentials'
                },
                auth=(self.client_id, self.client_secret),
                verify=False)
            js = resp.json()
            return js.get('access_token').encode()
        except:
            raise InvalidToken()

    @property
    def bearer(self):
        return self._bearer


    def upload_csr(self, data):
        pass


    def _get_domain_id(self, name):
        encoded_name = urllib.urlencode(name)
        get_domain = requests.get(self.base_url+'/domains.json?name=%s'%encoded_name,
            headers={'Authorization': 'Bearer '+self.bearer}, 
            verify=False)
        tree = html.fromstring(get_domain.text)
        tree.xpath()
        return

    def download_crt(self, id=None):
        return 'dsjjsdhfbiusehgf9s8yr9783h9'
        id = id if id else self.id
        get_cert = requests.get(self.base_url+'/api/crt/%s'%id)
        return base64.b64decode(get_cert.json()['crt'])
