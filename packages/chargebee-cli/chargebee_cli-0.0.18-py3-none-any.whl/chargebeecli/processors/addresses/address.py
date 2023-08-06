from chargebeecli.client.actionsImpl import ActionsImpl
from chargebeecli.export.Exporter import Exporter
from chargebeecli.processor import Processor
from chargebeecli.response_formatter import ResponseFormatter
from chargebeecli.util.printer import custom_print, custom_print_error
from chargebeecli.validator import Validator

API_URI = '/api/v2/addresses'


class Address(Processor, Validator, ResponseFormatter, Exporter):
    __action_processor = ActionsImpl()

    def __init__(self, export_format=None, export_path=None, file_name=None):
        self.headers = self.get_api_header()
        self.export_format = export_format
        self.export_path = export_path
        self.file_name = file_name
        self.tables = None

    def validate_param(self, __input_columns):
        self.headers = super().validate_param(__input_columns, self.headers)
        return self

    def get_api_header(self):
        return ["addr", "city", "country", "first_name", "label", "last_name", "object", "state", "state_code",
                "subscription_id", "validation_status", "zip"]

    def format(self, __format, __operation):
        super().format(self.response, __format, __operation, self.headers, 'address', 'list')
        return self

    def process(self, ctx, operation, payload, resource_id):
        return super(Address, self).process(ctx, operation, payload, resource_id)

    def get(self, ctx, payload, resource_id):
        return self.__action_processor.get(API_URI + '/' + resource_id)

    def list(self, ctx):
        custom_print_error('list: operation is not supported for addresses')
        exit()

    def delete(self, ctx, payload, resource_id):
        custom_print_error('operation is not supported..')
        exit()


    def to_be_exported(self):
        return self.export_format and self.export_path and self.file_name

    def export_data(self):
        if self.to_be_exported():
            Exporter(self.headers, self.tables).export(_path=self.export_path, _export_format=self.export_format,
                                                       _file_name=self.file_name)
