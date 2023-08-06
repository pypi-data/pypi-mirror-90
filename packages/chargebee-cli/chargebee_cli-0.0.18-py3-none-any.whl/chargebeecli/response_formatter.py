import json

import click
from tabulate import tabulate

from chargebeecli.constants.constants import Formats, ERROR_HEADER


class ResponseFormatter(object):

    def format(self, __format, __operation):
        raise NotImplementedError("Please Implement this method")

    def format(self, __response, __format, __operation, __headers, __resource_type, __list_key='list'):
        if __response.status_code != 200:
            if __format.lower() != Formats.JSON.value.lower():
                return self.__create_table(__response, __format, __operation, ERROR_HEADER, None, None)
            click.echo(click.style(__response.content.decode('utf-8'), fg="red"))
            return self

        if __format.lower() == Formats.JSON.value.lower():
            click.echo(__response.content)
            return self

        return self.__create_table(__response, __format, __operation, __headers, __resource_type, __list_key)

    def __create_table(self, __response, __format, __operation, __headers, __resource_type, __list_key):
        table = []
        tables = []
        if __operation == __list_key:
            subscriptions = json.loads(__response.content.decode('utf-8'))[__list_key]
            for __subscription in subscriptions:
                __subscription = __subscription[__resource_type]
                table = []
                for header in __headers:
                    s = __subscription.get(header, None)
                    table.append(s)
                tables.append(table)
        else:
            if __resource_type is None:
                data = json.loads(__response.content.decode('utf-8'))
            else:
                data = json.loads(__response.content.decode('utf-8'))[__resource_type]
            for header in __headers:
                table.append(data.get(header, None))
            tables.append(table)
        click.echo(tabulate(tables, __headers, tablefmt="grid", stralign="center", showindex=True))
        return tables
