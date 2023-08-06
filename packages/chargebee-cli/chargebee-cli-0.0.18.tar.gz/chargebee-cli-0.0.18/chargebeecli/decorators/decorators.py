import click

from chargebeecli.constants.constants import Export_Formats
from chargebeecli.models.models import Export_Params


def export_options(func):
    @click.option('--export-format',"-ef", help='data to be imported in [csv / excel / html',
                  default=Export_Formats.CSV.value, type=str)
    @click.option('--export-filename', "-ef",help='name of exported file', type=str)
    def call_export_option(export_format, export_filename, **kwargs):
        kwargs['export_params'] = Export_Params(export_format, export_filename, None)
        func(**kwargs)

    return call_export_option


class Magic():
    def __init__(self, magic_foo, magic_bar):
        self.magic = magic_foo
        self.color = magic_bar


def magic_options(func):
    @click.option('--magic-bar')
    @click.option('--magic-foo')
    def distill_magic(magic_foo, magic_bar, **kwargs):
        kwargs['magic1'] = Magic(magic_foo, magic_bar)
        func(**kwargs)

    return distill_magic
