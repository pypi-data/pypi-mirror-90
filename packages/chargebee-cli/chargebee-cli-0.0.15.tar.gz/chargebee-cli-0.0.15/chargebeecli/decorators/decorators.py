import click

from chargebeecli.constants.constants import Export_Formats


def export_option(func):
    @click.option('--export-format', "-ef", help='data to be imported in [csv / excel / html',
                  default=Export_Formats.CSV.value, type=str)
    @click.option('--export-filename', "-efn", help='name of exported file', type=str)
    @click.option('--export-path', "-ep", help='path where file to be exported', type=click.File('wb'))
    def call_export_option( export_format, export_path, **kwargs):
        kwargs['export'] = {'export_format': export_format, 'export_filename': 'export_filename',
                            'export_path': export_path}
        func(**kwargs)

    return call_export_option
