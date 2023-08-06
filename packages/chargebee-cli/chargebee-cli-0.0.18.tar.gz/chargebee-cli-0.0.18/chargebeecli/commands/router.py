import click
import pyfiglet


from .. import profile_configurator, login_processor
from ..constants.constants import Formats, Export_Formats
from ..processors.addons.addons import Addons
from ..processors.addresses.address import Address
from ..processors.cards.card import Card
from ..processors.comments.comment import Comment
from ..processors.coupon_codes.coupon_code import CouponCode
from ..processors.coupon_sets.coupon_sets import CouponSet
from ..processors.coupons.coupons import Coupons
from ..processors.credit_notes.credit_note import CreditNote
from ..processors.customer.customer import Customer
from ..processors.events.events import Event
from ..processors.exports.export import Export
from ..processors.hosted_pages.hosted_pages import HostedPage
from ..processors.invoices.invoice import Invoice
from ..processors.order.order import Order
from ..processors.plan.plan import Plan
from ..processors.profile.profile import Profile
from ..processors.promotional_credits.promotional_credit import PromotionalCredit
from ..processors.quotes.quote import Quote
from ..processors.subs.subscriptions import Subscription
from ..processors.transactions.transaction import Transaction
from ..processors.unbilled_chrages.unbilled_charge import UnbilledCharge
from ..util import version_util
from ..util.multiple_columns import MultipleColumns
from ..util.printer import custom_print


def safe_entry_point():
    # try:
    entry_point()


# except Exception as e:
#     print(Fore.RED, '------------------------------------------')
#     print(Fore.RED, 'unable to process../ COMMAND NOT NOT FOUND',e)
#     print(Fore.RED, '------------------------------------------')
#     exit(0)

def get_cmd_help():
    return "------------------------------------------------------------------------\nunleash the power of chargebee " \
           "apis from your command prompt.					\n for api reference: " \
           "https://apidocs.chargebee.com/docs/api?prod_cat_ver=1 ] 	" \
           "\n-------------------------------------------------------------------------- "


@click.group(help=get_cmd_help())
@click.pass_context
def entry_point(ctx):
    """unleash the power of chargebee apis from your command prompt.
    for api reference: [ https://apidocs.chargebee.com/docs/api?prod_cat_ver=1 ]"""


# info cmd
@entry_point.command("info")
@click.pass_context
def info(ctx):
    """Get the information about chargebee-cli ."""
    result = pyfiglet.figlet_format("chargebee-cli", font="slant")
    click.echo(result)


# cmd 1
@entry_point.group(help='configure the local resources like profile.')
@click.pass_context
def configure(ctx):
    pass


@configure.command("profile", help='configure new profile')
@click.pass_context
@click.option("--name", '-n', type=str, required=True)
@click.option("--api-key", '-ak', type=str, required=True)
@click.option("--account", '-a', type=str, required=True)
def configure_profile_cmd(ctx, name, api_key, account):
    profile_configurator.process(name, {'api_key': api_key, 'account': account})


# profile command
@entry_point.command("profile", help='manage credentials for local chargebee profiles')
@click.pass_context
@click.option("--operation", "-op", required=True, type=str)
@click.option("--name", "-n", help="profile name", required=False, type=str)
@click.option("--format", "-f", required=False,
              help="this allows user to format the output in json or table format..", default=Formats.TABLE.name)
@click.option('--columns', '-cols', nargs=0, required=False, help="columns to be printed in output")
@click.argument('columns', nargs=-1)
def profile(ctx, operation, columns, format, name):
    Profile() \
        .validate_param(columns) \
        .process(None, operation, payload=None, resource_id=name) \
        .format(format, operation)


# login command
@entry_point.command("login", help='login to the profile')
@click.pass_context
@click.option("--profile", "-p", required=True, type=str)
def login(ctx, profile):
    login_processor.process(profile)


# plan start cmd
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
def plan(ctx, id, operation, columns, format, name, invoice_name, price, export_filename, export_format, export_path):
    Plan(export_format=export_format, export_path=export_path, file_name=export_filename, response_format=format ) \
        .validate_param(columns) \
        .process(None, operation, payload=None, resource_id=id) \
        .format(format, operation) \
        .export_data()
    ctx.exit()


# plan end
@entry_point.resultcallback()
def process_result(result):
    custom_print("\n.................................end.................................")
    return result


# addons start cmd
@entry_point.command("addon", help='endpoint to perform operation on addon resource')
@click.pass_context
@click.option("--id", "-i", help="addon id", required=False, type=str)
@click.option("--operation", "-op", required=True,
              help=" operation to be executed, like fetch/create/update/delete.. ")
@click.option('--columns', '-cols', nargs=0, required=False, help="columns to be printed in output")
@click.option("--format", "-f", required=False,
              help="this allows user to format the output in json or table format..", default=Formats.TABLE.name)
@click.argument('columns', nargs=-1)
@click.option('--export-format', "-ef", help='data to be imported in [csv / excel / html',
              default=Export_Formats.CSV.value, type=str)
@click.option('--export-filename', "-efn", help='name of exported file', type=str)
@click.option('--export-path', "-ep", help='path where file to be exported', type=click.Path(exists=True))
def addon(ctx, id, operation, columns, format, export_filename, export_format, export_path):
    Addons() \
        .validate_param(columns) \
        .process(None, operation, payload=None, resource_id=id) \
        .format(format, operation)


# addons end


# coupons start cmd
@entry_point.command("coupon", help='endpoint to perform operation on coupon resource')
@click.pass_context
@click.option("--id", "-i", help="coupon id", required=False, type=str)
@click.option("--operation", "-op", required=True,
              help=" operation to be executed, like fetch/create/update/delete.. ")
@click.option('--columns', '-cols', nargs=0, required=False, help="columns to be printed in output")
@click.option("--format", "-f", required=False,
              help="this allows user to format the output in json or table format..", default=Formats.TABLE.name)
@click.argument('columns', nargs=-1)
@click.option('--export-format', "-ef", help='data to be imported in [csv / excel / html',
              default=Export_Formats.CSV.value, type=str)
@click.option('--export-filename', "-efn", help='name of exported file', type=str)
@click.option('--export-path', "-ep", help='path where file to be exported', type=click.Path(exists=True))
def coupon(ctx, id, operation, columns, format, export_filename, export_format, export_path):
    Coupons() \
        .validate_param(columns) \
        .process(None, operation, payload=None, resource_id=id) \
        .format(format, operation)


# coupons end

# customer start cmd
@entry_point.command("customer", help='endpoint to perform operation on [customer] resource')
@click.pass_context
@click.option("--id", "-i", help="customer id", required=False, type=str)
@click.option("--operation", "-op", required=True,
              help=" operation to be executed, like fetch/create/update/delete.. ")
@click.option('--columns', '-cols', nargs=0, required=False, help="columns to be printed in output")
@click.option("--format", "-f", required=False,
              help="this allows user to format the output in json or table format..", default=Formats.TABLE.name)
@click.argument('columns', nargs=-1)
@click.option('--export-format', "-ef", help='data to be imported in [csv / excel / html',
              default=Export_Formats.CSV.value, type=str)
@click.option('--export-filename', "-efn", help='name of exported file', type=str)
@click.option('--export-path', "-ep", help='path where file to be exported', type=click.Path(exists=True))
def customer(ctx, id, operation, columns, format, export_filename, export_format, export_path):
    Customer(export_format=export_format, export_path=export_path, file_name=export_filename, response_format=format) \
        .validate_param(columns) \
        .process(None, operation, payload=None, resource_id=id) \
        .format(format, operation) \
        .export_data()


# coupons end

@entry_point.command("export", help='export the data using cmd')
@click.pass_context
@click.option("--id", "-i", help="export id", required=False, type=str)
@click.option("--operation", "-op", required=True,
              help=" operation to be executed, like fetch/create/update/delete.. ")
@click.option('--columns', '-cols', nargs=0, required=False, help="columns to be printed in output")
@click.option("--format", "-f", required=False,
              help="this allows user to format the output in json or table format..", default=Formats.TABLE.name)
@click.argument('columns', nargs=-1)
def export(ctx, id, operation, columns, format):
    Export() \
        .validate_param(columns) \
        .process(None, operation, payload=None, resource_id=id) \
        .format(format, operation)


# subscription start cmd
@entry_point.command(name="subs", help='endpoint to perform operation on [subscription] resource')
@click.pass_context
@click.option("--id", "-i", help="subscription id", required=False, type=str)
@click.option("--operation", "-op", required=True,
              help=" operation to be executed, like fetch/create/update/delete.. ")
@click.option("--format", "-f", required=False,
              help="this allows user to format the output in json or table format..", default=Formats.TABLE.name,
              show_default=True)
@click.option('--columns-subs', "-s", nargs=-1, required=False, help="columns to be printed in output",
              cls=MultipleColumns)
@click.option('--columns-cus', "-c", nargs=-1, required=False, help="columns to be printed in output",
              cls=MultipleColumns)
@click.option('--export-format', "-ef", help='data to be imported in [csv / excel / html',
              default=Export_Formats.CSV.value, type=str)
@click.option('--export-filename', "-efn", help='name of exported file', type=str)
@click.option('--export-path', "-ep", help='path where file to be exported', type=click.Path(exists=True))
def subscription(ctx, id, operation, columns_subs, columns_cus, format, export_filename, export_format, export_path):
    Subscription(columns_subs, columns_cus, operation) \
        .validate_param(columns_subs) \
        .process(None, operation, payload=None, resource_id=id) \
        .format(format, operation) \
        .format_customer(format, operation)


# coupons end

# cards start cmd
@entry_point.command("card", help='endpoint to perform operation on [card] resource')
@click.pass_context
@click.option("--id", "-i", help="customer id", required=False, type=str)
@click.option("--operation", "-op", required=True,
              help=" operation to be executed, like fetch/create/update/delete.. ")
@click.option('--columns', '-cols', nargs=0, required=False, help="columns to be printed in output")
@click.option("--format", "-f", required=False,
              help="this allows user to format the output in json or table format..", default=Formats.TABLE.name)
@click.argument('columns', nargs=-1)
@click.option('--export-format', "-ef", help='data to be imported in [csv / excel / html',
              default=Export_Formats.CSV.value, type=str)
@click.option('--export-filename', "-efn", help='name of exported file', type=str)
@click.option('--export-path', "-ep", help='path where file to be exported', type=click.Path(exists=True))
def cards(ctx, id, operation, columns, format, export_filename, export_format, export_path):
    Card() \
        .validate_param(columns) \
        .process(None, operation, payload=None, resource_id=id) \
        .format(format, operation)


@entry_point.command("promotional_credit", help='endpoint to perform operation on [promotional_credit] resource')
@click.pass_context
@click.option("--id", "-i", help="customer id", required=False, type=str)
@click.option("--operation", "-op", required=True,
              help=" operation to be executed, like fetch/create/update/delete.. ")
@click.option('--columns', '-cols', nargs=0, required=False, help="columns to be printed in output")
@click.option("--format", "-f", required=False,
              help="this allows user to format the output in json or table format..", default=Formats.TABLE.name)
@click.argument('columns', nargs=-1)
@click.option('--export-format', "-ef", help='data to be imported in [csv / excel / html',
              default=Export_Formats.CSV.value, type=str)
@click.option('--export-filename', "-efn", help='name of exported file', type=str)
@click.option('--export-path', "-ep", help='path where file to be exported', type=click.Path(exists=True))
def promotional_credits(ctx, id, operation, columns, format, export_filename, export_format, export_path):
    PromotionalCredit() \
        .validate_param(columns) \
        .process(None, operation, payload=None, resource_id=id) \
        .format(format, operation)


@entry_point.command("invoice", help='endpoint to perform operation on [invoice] resource')
@click.pass_context
@click.option("--id", "-i", help="invoice id", required=False, type=str)
@click.option("--operation", "-op", required=True,
              help=" operation to be executed, like fetch/create/update/delete.. ")
@click.option('--columns', '-cols', nargs=0, required=False, help="columns to be printed in output")
@click.option("--format", "-f", required=False,
              help="this allows user to format the output in json or table format..", default=Formats.TABLE.name)
@click.argument('columns', nargs=-1)
@click.option('--export-format', "-ef", help='data to be imported in [csv / excel / html',
              default=Export_Formats.CSV.value, type=str)
@click.option('--export-filename', "-efn", help='name of exported file', type=str)
@click.option('--export-path', "-ep", help='path where file to be exported', type=click.Path(exists=True))
def invoice(ctx, id, operation, columns, format, export_filename, export_format, export_path):
    Invoice() \
        .validate_param(columns) \
        .process(None, operation, payload=None, resource_id=id) \
        .format(format, operation)


@entry_point.command("credit_note", help='endpoint to perform operation on [credit_note] resource')
@click.pass_context
@click.option("--id", "-i", help="credit_note id", required=False, type=str)
@click.option("--operation", "-op", required=True,
              help=" operation to be executed, like fetch/create/update/delete.. ")
@click.option('--columns', '-cols', nargs=0, required=False, help="columns to be printed in output")
@click.option("--format", "-f", required=False,
              help="this allows user to format the output in json or table format..", default=Formats.TABLE.name)
@click.argument('columns', nargs=-1)
@click.option('--export-format', "-ef", help='data to be imported in [csv / excel / html',
              default=Export_Formats.CSV.value, type=str)
@click.option('--export-filename', "-efn", help='name of exported file', type=str)
@click.option('--export-path', "-ep", help='path where file to be exported', type=click.Path(exists=True))
def credit_note(ctx, id, operation, columns, format, export_filename, export_format, export_path):
    CreditNote() \
        .validate_param(columns) \
        .process(None, operation, payload=None, resource_id=id) \
        .format(format, operation)


@entry_point.command("unbilled_charge", help='endpoint to perform operation on [unbilled_charge] resource')
@click.pass_context
@click.option("--id", "-i", help="credit_note id", required=False, type=str)
@click.option("--operation", "-op", required=True,
              help=" operation to be executed, like fetch/create/update/delete.. ")
@click.option('--columns', '-cols', nargs=0, required=False, help="columns to be printed in output")
@click.option("--format", "-f", required=False,
              help="this allows user to format the output in json or table format..", default=Formats.TABLE.name)
@click.argument('columns', nargs=-1)
@click.option('--export-format', "-ef", help='data to be imported in [csv / excel / html',
              default=Export_Formats.CSV.value, type=str)
@click.option('--export-filename', "-efn", help='name of exported file', type=str)
@click.option('--export-path', "-ep", help='path where file to be exported', type=click.Path(exists=True))
def unbilled_charges(ctx, id, operation, columns, format, export_filename, export_format, export_path):
    UnbilledCharge() \
        .validate_param(columns) \
        .process(None, operation, payload=None, resource_id=id) \
        .format(format, operation)


@entry_point.command("order", help='endpoint to perform operation on [order] resource')
@click.pass_context
@click.option("--id", "-i", help="order id", required=False, type=str)
@click.option("--operation", "-op", required=True,
              help=" operation to be executed, like fetch/create/update/delete.. ")
@click.option('--columns', '-cols', nargs=0, required=False, help="columns to be printed in output")
@click.option("--format", "-f", required=False,
              help="this allows user to format the output in json or table format..", default=Formats.TABLE.name)
@click.argument('columns', nargs=-1)
@click.option('--export-format', "-ef", help='data to be imported in [csv / excel / html',
              default=Export_Formats.CSV.value, type=str)
@click.option('--export-filename', "-efn", help='name of exported file', type=str)
@click.option('--export-path', "-ep", help='path where file to be exported', type=click.Path(exists=True))
def order(ctx, id, operation, columns, format, export_filename, export_format, export_path):
    Order() \
        .validate_param(columns) \
        .process(None, operation, payload=None, resource_id=id) \
        .format(format, operation)


@entry_point.command("gift", help='endpoint to perform operation on [gift] resource')
@click.pass_context
@click.option("--id", "-i", help="order id", required=False, type=str)
@click.option("--operation", "-op", required=True,
              help=" operation to be executed, like fetch/create/update/delete.. ")
@click.option('--columns', '-cols', nargs=0, required=False, help="columns to be printed in output")
@click.option("--format", "-f", required=False,
              help="this allows user to format the output in json or table format..", default=Formats.TABLE.name)
@click.argument('columns', nargs=-1)
def order(ctx, id, operation, columns, format):
    Order() \
        .validate_param(columns) \
        .process(None, operation, payload=None, resource_id=id) \
        .format(format, operation)


@entry_point.command("txn", help='endpoint to perform operation on [Transaction] resource')
@click.pass_context
@click.option("--id", "-i", help="txn id", required=False, type=str)
@click.option("--operation", "-op", required=True,
              help=" operation to be executed, like fetch/create/update/delete.. ")
@click.option('--columns', '-cols', nargs=0, required=False, help="columns to be printed in output")
@click.option("--format", "-f", required=False,
              help="this allows user to format the output in json or table format..", default=Formats.TABLE.name)
@click.argument('columns', nargs=-1)
def txn(ctx, id, operation, columns, format):
    Transaction() \
        .validate_param(columns) \
        .process(None, operation, payload=None, resource_id=id) \
        .format(format, operation)


@entry_point.command("hosted_page", help='endpoint to perform operation on [hosted_page] resource')
@click.pass_context
@click.option("--id", "-i", help="hosted_pages id", required=False, type=str)
@click.option("--operation", "-op", required=True,
              help=" operation to be executed, like fetch/create/update/delete.. ")
@click.option('--columns', '-cols', nargs=0, required=False, help="columns to be printed in output")
@click.option("--format", "-f", required=False,
              help="this allows user to format the output in json or table format..", default=Formats.TABLE.name)
@click.argument('columns', nargs=-1)
def hosted_pages(ctx, id, operation, columns, format):
    HostedPage() \
        .validate_param(columns) \
        .process(None, operation, payload=None, resource_id=id) \
        .format(format, operation)


@entry_point.command("quote", help='endpoint to perform operation on [quote] resource')
@click.pass_context
@click.option("--id", "-i", help="quote id", required=False, type=str)
@click.option("--operation", "-op", required=True,
              help=" operation to be executed, like fetch/create/update/delete.. ")
@click.option('--columns', '-cols', nargs=0, required=False, help="columns to be printed in output")
@click.option("--format", "-f", required=False,
              help="this allows user to format the output in json or table format..", default=Formats.TABLE.name)
@click.argument('columns', nargs=-1)
def quote(ctx, id, operation, columns, format):
    Quote() \
        .validate_param(columns) \
        .process(None, operation, payload=None, resource_id=id) \
        .format(format, operation)


@entry_point.command("coupon_set", help='endpoint to perform operation on [coupon_set] resource')
@click.pass_context
@click.option("--id", "-i", help="coupon_set id", required=False, type=str)
@click.option("--operation", "-op", required=True,
              help=" operation to be executed, like fetch/create/update/delete.. ")
@click.option('--columns', '-cols', nargs=0, required=False, help="columns to be printed in output")
@click.option("--format", "-f", required=False,
              help="this allows user to format the output in json or table format..", default=Formats.TABLE.name)
@click.argument('columns', nargs=-1)
def coupon_set(ctx, id, operation, columns, format):
    CouponSet() \
        .validate_param(columns) \
        .process(None, operation, payload=None, resource_id=id) \
        .format(format, operation)


@entry_point.command("coupon_code", help='endpoint to perform operation on [coupon_code] resource')
@click.pass_context
@click.option("--id", "-i", help="coupon_code id", required=False, type=str)
@click.option("--operation", "-op", required=True,
              help=" operation to be executed, like fetch/create/update/archive.. ")
@click.option('--columns', '-cols', nargs=0, required=False, help="columns to be printed in output")
@click.option("--format", "-f", required=False,
              help="this allows user to format the output in json or table format..", default=Formats.TABLE.name)
@click.argument('columns', nargs=-1)
def coupon_code(ctx, id, operation, columns, format):
    """ endpoint to perform operation on coupon resources."""
    if operation == 'archive':
        operation = 'delete'

    CouponCode() \
        .validate_param(columns) \
        .process(None, operation, payload=None, resource_id=id) \
        .format(format, operation)


@entry_point.command("address", help='endpoint to perform operation on [address] resource')
@click.pass_context
@click.option("--id", "-i", help="address id", required=False, type=str)
@click.option("--operation", "-op", required=True,
              help=" operation to be executed, like fetch/create/update/delete.. ")
@click.option('--columns', '-cols', nargs=0, required=False, help="columns to be printed in output")
@click.option("--format", "-f", required=False,
              help="this allows user to format the output in json or table format..", default=Formats.TABLE.name)
@click.argument('columns', nargs=-1)
def address(ctx, id, operation, columns, format):
    Address() \
        .validate_param(columns) \
        .process(None, operation, payload=None, resource_id=id) \
        .format(format, operation)


@entry_point.command("event", help='endpoint to perform operation on [event] resource')
@click.pass_context
@click.option("--id", "-i", help="event id", required=False, type=str)
@click.option("--operation", "-op", required=True,
              help=" operation to be executed, like fetch/create/update/delete.. ")
@click.option('--columns', '-cols', nargs=0, required=False, help="columns to be printed in output")
@click.option("--format", "-f", required=False,
              help="this allows user to format the output in json or table format..", default=Formats.TABLE.name)
@click.argument('columns', nargs=-1)
def event(ctx, id, operation, columns, format):
    Event() \
        .validate_param(columns) \
        .process(None, operation, payload=None, resource_id=id) \
        .format(format, operation)


@entry_point.command("comment", help='endpoint to perform operation on [comment] resource')
@click.pass_context
@click.option("--id", "-i", help="comment id", required=False, type=str)
@click.option("--operation", "-op", required=True,
              help=" operation to be executed, like fetch/create/update/delete.. ")
@click.option('--columns', '-cols', nargs=0, required=False, help="columns to be printed in output")
@click.option("--format", "-f", required=False,
              help="this allows user to format the output in json or table format..", default=Formats.TABLE.name)
@click.argument('columns', nargs=-1)
def comment(ctx, id, operation, columns, format):
    Comment() \
        .validate_param(columns) \
        .process(None, operation, payload=None, resource_id=id) \
        .format(format, operation)


# feedback command
@entry_point.command("feedback", help='provide the feedback')
@click.pass_context
@click.option("--output-format", "-of", default='table', type=str, required=False)
def feedback(ctx, output_format):
    pass
