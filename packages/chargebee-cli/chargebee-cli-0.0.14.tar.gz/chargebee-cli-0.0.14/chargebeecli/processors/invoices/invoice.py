from chargebeecli.client.actionsImpl import ActionsImpl
from chargebeecli.printer import Printer
from chargebeecli.processor import Processor
from chargebeecli.response_formatter import ResponseFormatter
from chargebeecli.validator import Validator

API_URI = '/api/v2/invoices'


class Invoice(Processor, Validator, ResponseFormatter, Printer):
    __action_processor = ActionsImpl()

    def __init__(self):
        self.headers = self.get_api_header()

    def validate_param(self, __input_columns):
        self.headers = super().validate_param(__input_columns, self.headers)
        return self

    def get_api_header(self):
        return ["adjustment_credit_notes", "amount_adjusted", "amount_due", "amount_paid", "amount_to_collect",
                "applied_credits", "base_currency_code", "billing_address", "credits_applied", "currency_code",
                "customer_id", "date", "deleted", "due_date", "dunning_attempts", "exchange_rate", "first_invoice",
                "has_advance_charges", "id", "is_gifted", "issued_credit_notes", "line_items", "linked_orders",
                "linked_payments", "net_term_days", "new_sales_amount", "object", "paid_at", "price_type", "recurring",
                "resource_version", "round_off_amount", "status", "sub_total", "tax", "term_finalized", "total",
                "updated_at", "write_off_amount"]

    def format(self, __format, __operation):
        super().format(self.response, __format, __operation, self.headers, 'invoice', 'list')
        return self

    def process(self, ctx, operation, payload, resource_id):
        return super(Invoice, self).process(ctx, operation, payload, resource_id)

    def get(self, ctx, payload, resource_id):
        return self.__action_processor.get(API_URI + '/' + resource_id)

    def list(self, ctx):
        return self.__action_processor.get(API_URI)

    def delete(self, ctx, payload, resource_id):
        return self.__action_processor.delete(API_URI + '/' + resource_id + '/' + 'delete')
