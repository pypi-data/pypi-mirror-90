from chargebeecli.commands.command import Command


class Plan(Command):

    def __init__(self):
        pass

    def get_help_text(self):
        return "Manage plan resource!!!"

    def get_command_name(self):
        return "plan"

    def get_options(self):
        pass

    def get_arguments(self):
        pass


"""
@entry_point.command(name="plan", help='endpoint to perform operation on plan resource')
@click.pass_context
@click.option("--id", "-i", help="plan id", required=False, type=str)
@click.option("--name", "-n", help="plan name", required=False, type=str)
@click.option("--invoice-name", "-in", help="invoice name", required=False, type=str)
@click.option("--price", "-p", help="plan price", required=False, type=int)
@click.option("--operation", "-op", required=True,
              help="operation to be executed,like [list/fetch/create/update/delete]")
@click.option("--format", "-f", required=False,
              help="this allows user to format the output in json or table format..", default=Formats.TABLE.name)
@click.option('--columns', '-cols', nargs=0, required=False, help="columns to be printed in output")
@click.argument('columns', nargs=-1)
@click.option('--export-format', "-ef", help='data to be imported in [csv / excel / html',
              default=Export_Formats.CSV.value, type=str)
@click.option('--export-filename', "-efn", help='name of exported file', type=str)
@click.option('--export-path', "-ep", help='path where file to be exported', type=click.Path(exists=True))
"""