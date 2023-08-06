from chargebeecli.client.actionsImpl import ActionsImpl
from chargebeecli.printer import Printer
from chargebeecli.processor import Processor
from chargebeecli.response_formatter import ResponseFormatter
from chargebeecli.validator import Validator

API_URI = '/api/v2/customers'


class Customer(Processor, Validator, ResponseFormatter, Printer):
    __action_processor = ActionsImpl()

    def __init__(self):
        self.headers = self.get_api_header()

    def validate_param(self, __input_columns):
        self.headers = super().validate_param(__input_columns, self.headers)
        return self

    def get_api_header(self):
        return ["id", "first_name", "email", "auto_collection", "net_term_days", "allow_direct_debit", "created_at",
                "taxability", "updated_at", "pii_cleared", "resource_version", "deleted", "object", "card_status",
                "promotional_credits", "refundable_credits", "excess_payments", "unbilled_charges",
                "preferred_currency_code", "primary_payment_source_id", "payment_method"]

    def format(self, __format, __operation):
        super().format(self.response, __format, __operation, self.headers, 'customer', 'list')
        return self

    def process(self, ctx, operation, payload, resource_id):
        return super(Customer, self).process(ctx, operation, payload, resource_id)

    def get(self, ctx, payload, resource_id):
        return self.__action_processor.get(API_URI + '/' + resource_id)

    def list(self, ctx):
        return self.__action_processor.get(API_URI)

    def delete(self, ctx, payload, resource_id):
        return self.__action_processor.delete(API_URI + '/' + resource_id + '/' + 'delete')
