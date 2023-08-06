import pandas as pd
import openpyxl
from chargebeecli.constants.constants import Export_Formats, Export_Formats_Extensions
import click
from pathlib import Path
import os

from chargebeecli.util.printer import custom_print, custom_print_error

_DEFAULT_OUTPUT_FILE_NAME = 'result'

_DEFAULT_EXCEL_SHEET_NAME = 'sheet'


def _get_compression_options(__compression, __file_name=_DEFAULT_OUTPUT_FILE_NAME):
    if __compression:
        return dict(method='zip', archive_name=__file_name)
    return None


def _is_format_accepted(export_format):
    if export_format in list(map(str, Export_Formats.value)):
        return True
    return False


class Exporter(object):

    def __init__(self, headers, data):
        self.headers = headers
        self.data = data
        self.df = pd.DataFrame(self.data, columns=self.headers)

    def to_be_exported(self):
        raise NotImplementedError("Please Implement this method")

    def export(self, _path, _export_format, _file_name=_DEFAULT_OUTPUT_FILE_NAME, compression=False):
        try:
            if Export_Formats.CSV.value.lower() == _export_format.lower():
                self.export_csv(path=_path, _file_name=_file_name, compression=_get_compression_options(compression))
            elif Export_Formats.EXCEL.value.lower() == _export_format.lower():
                self.export_excel(path=_path, _file_name=_file_name)
            elif Export_Formats.HTML.value.lower() == _export_format.lower():
                self.export_html(path=_path, _file_name=_file_name)
            else:
                click.echo('format not supported')
                exit()

            custom_print('!!!  exported !!')
        except Exception as e:
            custom_print_error(e)

    def export_csv(self, path, _file_name, compression):
        self.df.to_csv(Path(os.path.join(path, _file_name + Export_Formats_Extensions.CSV.value)),
                       compression=compression, index=False)

    def export_excel(self, _file_name, path):
        self.df.to_excel(os.path.join(path, _file_name + Export_Formats_Extensions.EXCEL.value),
                         sheet_name=_DEFAULT_EXCEL_SHEET_NAME,
                         index=False)

    def export_html(self, _file_name, path):
        self.df.to_html(Path(os.path.join(path, _file_name + Export_Formats_Extensions.HTML.value)),
                        classes='table-striped', index=False)
