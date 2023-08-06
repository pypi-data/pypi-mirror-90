import base64
import requests

from chargebeecli.Configuration import Configuration
from chargebeecli.client.actions import Actions


class ActionsImpl(Actions):

    def get(self, uri, params=None):
        config_info = self.__header()
        return requests.get(config_info['account'] + uri, params, headers=config_info['api_key'])

    def create(self, uri, payload):
        config_info = self.__header()
        return requests.post(config_info['account'] + uri, data=payload, headers=config_info['api_key'])

    def delete(self, uri, payload=None):
        config_info = self.__header()
        return requests.post(config_info['account'] + uri, data=payload, headers=config_info['api_key'])

    def __header(self):
        config_data = Configuration.Instance().get_account_api_key()
        b64_val = base64.b64encode(('%s:' % config_data['api_key']).encode('latin1')).strip().decode('latin1')
        return {'api_key': {"Authorization": "Basic %s" % b64_val}, 'account': config_data['account']}
