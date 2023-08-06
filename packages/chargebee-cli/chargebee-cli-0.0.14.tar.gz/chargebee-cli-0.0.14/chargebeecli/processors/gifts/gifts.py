from chargebeecli.client.actionsImpl import ActionsImpl
from chargebeecli.printer import Printer
from chargebeecli.processor import Processor
from chargebeecli.response_formatter import ResponseFormatter
from chargebeecli.validator import Validator

API_URI = '/api/v2/gifts'


class Gift(Processor, Validator, ResponseFormatter, Printer):
    __action_processor = ActionsImpl()

    def __init__(self):
        self.headers = self.get_api_header()

    def validate_param(self, __input_columns):
        self.headers = super().validate_param(__input_columns, self.headers)
        return self

    def get_api_header(self):
        return ["auto_claim", "claim_expiry_date", "gift_receiver", "gift_timelines", "gifter", "id", "no_expiry",
                "object", "resource_version", "scheduled_at", "status", "updated_at"]

    def format(self, __format, __operation):
        super().format(self.response, __format, __operation, self.headers, 'gift', 'list')
        return self

    def process(self, ctx, operation, payload, resource_id):
        return super(Gift, self).process(ctx, operation, payload, resource_id)

    def get(self, ctx, payload, resource_id):
        return self.__action_processor.get(API_URI + '/' + resource_id)

    def list(self, ctx):
        return self.__action_processor.get(API_URI)

    def delete(self, ctx, payload, resource_id):
        return self.__action_processor.delete(API_URI + '/' + resource_id + '/' + 'cancel')
