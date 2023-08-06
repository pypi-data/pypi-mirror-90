import base64
import json

import click
import requests
from beautifultable import BeautifulTable
from colorama import init
from prettytable import PrettyTable
from tabulate import tabulate

from chargebeecli.Configuration import Configuration

init()


def header():
    config_data = Configuration.Instance().get_account_api_key()
    b64_val = base64.b64encode(('%s:' % config_data['api_key']).encode('latin1')).strip().decode('latin1')
    return {'api_key': {"Authorization": "Basic %s" % b64_val}, 'account': config_data['account']}


CHUNK_SIZE = 1024
configuration = Configuration.Instance()
configuration.update_section("active_profile", {'primary': 'dev'})

data = { "id":"silver5","name":"Silver5","applicable_addons":{"id":["sub_ssl"]},"price": 5000 }

r = requests.post(url='http://mannar-test.localcb.in:8080/api/v2/plans', headers=header()['api_key'], data = data)

# print(r.content.decode('utf-8'))
headers = ["id", "name", "price", "period", "period_unit", "trial_period", "trial_period_unit", "pricing_model",
           "free_quantity", "status", "enabled_in_hosted_pages", "enabled_in_portal", "addon_applicability",
           "is_shippable", "giftable", "object", "charge_model", "taxable", "currency_code",
           "show_description_in_invoices", "show_description_in_quotes"]

"""print tabulate([["value1", "value2"], ["value3", "value4"]], ["column 1", "column 2"], tablefmt="grid")
+------------+------------+
| column 1   | column 2   |
+============+============+
| value1     | value2     |
+------------+------------+
| value3     | value4     |
+------------+------------+"""



click.echo(json.loads(r.content.decode('utf-8')))

