from chargebeecli.client.actionsImpl import ActionsImpl
from chargebeecli.printer import Printer
from chargebeecli.processor import Processor
from chargebeecli.response_formatter import ResponseFormatter
from chargebeecli.validator import Validator

API_URI = '/api/v2/credit_notes'


class CreditNote(Processor, Validator, ResponseFormatter, Printer):
    __action_processor = ActionsImpl()

    def __init__(self):
        self.headers = self.get_api_header()

    def validate_param(self, __input_columns):
        self.headers = super().validate_param(__input_columns, self.headers)
        return self

    def get_api_header(self):
        return ["allocations", "amount_allocated", "amount_available", "amount_refunded", "base_currency_code",
                "create_reason_code", "currency_code", "customer_id", "date", "deleted", "exchange_rate",
                "fractional_correction", "id", "line_item_discounts", "line_item_taxes", "line_items", "linked_refunds",
                "object", "price_type", "reason_code", "reference_invoice_id", "resource_version", "round_off_amount",
                "status", "sub_total", "taxes", "total", "type", "updated_at"]

    def format(self, __format, __operation):
        super().format(self.response, __format, __operation, self.headers, 'credit_note', 'list')
        return self

    def process(self, ctx, operation, payload, resource_id):
        return super(CreditNote, self).process(ctx, operation, payload, resource_id)

    def get(self, ctx, payload, resource_id):
        return self.__action_processor.get(API_URI + '/' + resource_id)

    def list(self, ctx):
        return self.__action_processor.get(API_URI)

    def delete(self, ctx, payload, resource_id):
        return self.__action_processor.delete(API_URI + '/' + resource_id + '/' + 'delete')
