from chargebeecli.client.actionsImpl import ActionsImpl
from chargebeecli.constants.constants import ApiOperation
from chargebeecli.printer import Printer
from chargebeecli.processor import Processor
from chargebeecli.response_formatter import ResponseFormatter
from chargebeecli.validator import Validator

API_URI = '/api/v2/plans'


class Plan(Processor, Validator, ResponseFormatter, Printer):
    __action_processor = ActionsImpl()

    def __init__(self):
        self.headers = self.get_api_header()

    def validate_param(self, __input_columns):
        self.headers = super().validate_param(__input_columns, self.headers)
        return self

    def get_api_header(self):
        return ["id", "name", "price", "period", "period_unit", "trial_period", "trial_period_unit", "pricing_model",
                "free_quantity", "status", "enabled_in_hosted_pages", "enabled_in_portal", "addon_applicability",
                "is_shippable", "giftable", "object", "charge_model", "taxable", "currency_code",
                "show_description_in_invoices", "show_description_in_quotes"]

    def format(self, __format, __operation):
        super().format(self.response, __format, __operation, self.headers, 'plan', 'list')
        return self

    def process(self, ctx, operation, payload, resource_id):
        return super(Plan, self).process(ctx, operation, payload, resource_id)

    def get(self, ctx, payload, resource_id):
        return self.__action_processor.get(API_URI + '/' + resource_id)

    def create(self, ctx, payload, resource_id):
        return self.__action_processor.create(uri=API_URI, payload=payload)

    def list(self, ctx):
        return self.__action_processor.get(API_URI)

    def delete(self, ctx, payload, resource_id):
        return self.__action_processor.delete(API_URI + '/' + resource_id + '/' + 'delete')
