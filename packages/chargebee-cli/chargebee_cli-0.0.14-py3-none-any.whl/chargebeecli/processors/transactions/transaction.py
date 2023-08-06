from chargebeecli.client.actionsImpl import ActionsImpl
from chargebeecli.printer import Printer
from chargebeecli.processor import Processor
from chargebeecli.response_formatter import ResponseFormatter
from chargebeecli.validator import Validator

API_URI = '/api/v2/transactions'


class Transaction(Processor, Validator, ResponseFormatter, Printer):
    __action_processor = ActionsImpl()

    def __init__(self):
        self.headers = self.get_api_header()

    def validate_param(self, __input_columns):
        self.headers = super().validate_param(__input_columns, self.headers)
        return self

    def get_api_header(self):
        return ["amount", "amount_capturable", "authorization_reason", "base_currency_code", "currency_code",
                "customer_id", "date", "deleted", "exchange_rate", "fraud_reason", "gateway", "gateway_account_id",
                "id", "id_at_gateway", "linked_payments", "masked_card_number", "object", "payment_method",
                "payment_source_id", "resource_version", "status", "type", "updated_at"]

    def format(self, __format, __operation):
        super().format(self.response, __format, __operation, self.headers, 'transaction', 'list')
        return self

    def process(self, ctx, operation, payload, resource_id):
        return super(Transaction, self).process(ctx, operation, payload, resource_id)

    def get(self, ctx, payload, resource_id):
        return self.__action_processor.get(API_URI + '/' + resource_id)

    def list(self, ctx):
        return self.__action_processor.get(API_URI)
