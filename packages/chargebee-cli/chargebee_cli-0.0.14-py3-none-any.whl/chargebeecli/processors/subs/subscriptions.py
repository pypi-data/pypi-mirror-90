from chargebeecli.client.actionsImpl import ActionsImpl
from chargebeecli.printer import Printer
from chargebeecli.processor import Processor
from chargebeecli.processors.customer.subscription_customer import SubscriptionCustomer
from chargebeecli.response_formatter import ResponseFormatter
from chargebeecli.validator import Validator

API_URI = '/api/v2/subscriptions'


class Subscription(Processor, Validator, ResponseFormatter, Printer):
    __action_processor = ActionsImpl()

    def __init__(self, columns, columns_customer, operation):
        self.__columns = columns
        self.__operation = operation
        self.headers = self.get_api_header()
        self.__columns_customer = columns_customer
        self.__subscriptionCustomer = SubscriptionCustomer(columns_customer)
        self.headers_customer = self.__subscriptionCustomer.get_api_header()

    def validate_param(self, __input_columns):
        self.headers = super().validate_param(__input_columns, self.headers)
        self.headers_customer = super().validate_param(self.__columns_customer, self.headers_customer)
        return self

    def get_api_header(self):
        return ["activated_at", "auto_collection", "billing_period", "billing_period_unit", "created_at",
                "currency_code", "current_term_end", "current_term_start", "customer_id", "deleted",
                "due_invoices_count", "due_since", "has_scheduled_changes", "id", "mrr", "next_billing_at", "object",
                "plan_amount", "plan_free_quantity", "plan_id", "plan_quantity", "plan_unit_price", "resource_version",
                "started_at", "status", "total_dues", "updated_at"]

    def format(self, __format, __operation):
        super().format(self.response, __format, __operation,self.headers, 'subscription', 'list')
        return self

    def format_customer(self, __format, __operation):
        print("------------------")
        print("customer.............\n")
        print("------------------")
        super().format(self.response, __format, __operation, self.headers_customer,  'customer', 'list')
        return self

    def process(self, ctx, operation, payload, resource_id):
        return super(Subscription, self).process(ctx, operation, payload, resource_id)

    def get(self, ctx, payload, resource_id):
        return self.__action_processor.get(API_URI + '/' + resource_id)

    def list(self, ctx):
        return self.__action_processor.get(API_URI)

    def delete(self, ctx, payload, resource_id):
        return self.__action_processor.delete(API_URI + '/' + resource_id + '/' + 'delete')