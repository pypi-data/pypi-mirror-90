from chargebeecli.client.actionsImpl import ActionsImpl
from chargebeecli.printer import Printer
from chargebeecli.processor import Processor
from chargebeecli.response_formatter import ResponseFormatter
from chargebeecli.validator import Validator

API_URI = '/api/v2/hosted_pages'


class HostedPage(Processor, Validator, ResponseFormatter, Printer):
    __action_processor = ActionsImpl()

    def __init__(self):
        self.headers = self.get_api_header()

    def validate_param(self, __input_columns):
        self.headers = super().validate_param(__input_columns, self.headers)
        return self

    def get_api_header(self):
        return ["created_at", "embed", "expires_at", "id", "object", "resource_version", "state", "type", "updated_at",
                "url"]

    def format(self, __format, __operation):
        super().format(self.response, __format, __operation, self.headers, 'hosted_page', 'list')
        return self

    def process(self, ctx, operation, payload, resource_id):
        return super(HostedPage, self).process(ctx, operation, payload, resource_id)

    def get(self, ctx, payload, resource_id):
        return self.__action_processor.get(API_URI + '/' + resource_id)

    def list(self, ctx):
        return self.__action_processor.get(API_URI)
