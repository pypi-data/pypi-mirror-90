from chargebeecli.client.actionsImpl import ActionsImpl
from chargebeecli.constants.constants import Formats, ERROR_HEADER
from chargebeecli.export.Exporter import Exporter
from chargebeecli.processor import Processor
from chargebeecli.response_formatter import ResponseFormatter
from chargebeecli.validator import Validator

API_URI = '/api/v2/plans'


class Plan(Processor, Validator, ResponseFormatter, Exporter):
    __action_processor = ActionsImpl()

    def __init__(self, export_format, export_path, file_name, response_format):
        self.headers = self.get_api_header()
        self.export_format = export_format
        self.export_path = export_path
        self.file_name = file_name
        self.tables = None
        self.response_format = response_format

    def validate_param(self, __input_columns):
        self.headers = super().validate_param(__input_columns, self.headers)
        return self

    def get_api_header(self):
        return ["id", "name", "price", "period", "period_unit", "trial_period", "trial_period_unit", "pricing_model",
                "free_quantity", "status", "enabled_in_hosted_pages", "enabled_in_portal", "addon_applicability",
                "is_shippable", "giftable", "object", "charge_model", "taxable", "currency_code",
                "show_description_in_invoices", "show_description_in_quotes"]

    def process(self, ctx, operation, payload, resource_id):
        return super(Plan, self).process(ctx, operation, payload, resource_id)

    def format(self, __format, __operation):
        self.tables = super(Plan, self).format(self.response, __format, __operation, self.headers, 'plan', 'list')
        return self

    def get(self, ctx, payload, resource_id):
        return self.__action_processor.get(API_URI + '/' + resource_id)

    def create(self, ctx, payload, resource_id):
        return self.__action_processor.create(uri=API_URI, payload=payload)

    def list(self, ctx):
        return self.__action_processor.get(API_URI)

    def delete(self, ctx, payload, resource_id):
        return self.__action_processor.delete(API_URI + '/' + resource_id + '/' + 'delete')

    def to_be_exported(self):
        return self.export_format and self.export_path and self.file_name and \
               self.response_format.lower() == Formats.TABLE.value

    def export_data(self):
        if self.response.status_code != 200:
            self.headers = ERROR_HEADER
        if self.to_be_exported():
            Exporter(self.headers, self.tables).export(_path=self.export_path, _export_format=self.export_format,
                                                       _file_name=self.file_name)
