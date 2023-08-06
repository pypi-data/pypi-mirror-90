from chargebeecli.constants.constants import ApiOperation
from chargebeecli.constants.error_messages import OPERATION_NOT_SUPPORTED


class Processor(object):

    def get_api_header(self):
        raise NotImplementedError("Please Implement this method")

    def process(self, ctx, operation, payload, resource_id):
        if operation == ApiOperation.CREATE.value:
            self.response = self.create(ctx=ctx, payload=payload, resource_id=resource_id)
        elif operation ==  ApiOperation.FETCH.value:
            self.response = self.get(ctx=ctx, payload=payload, resource_id=resource_id)
        elif operation ==  ApiOperation.DELETE.value:
            self.response = self.delete(ctx=ctx, payload=payload, resource_id=resource_id)
        elif operation ==  ApiOperation.LIST.value:
            self.response = self.list(ctx=ctx)
        else:
            print(OPERATION_NOT_SUPPORTED)
            exit()
        return self

    def export_data(self):
        raise NotImplementedError("Please Implement this method")

    def get(self, ctx, payload, resource_id):
        raise NotImplementedError("Please Implement this method")

    def list(self, ctx):
        raise NotImplementedError("Please Implement this method")

    def create(self, ctx, payload, resource_id):
        raise NotImplementedError("Please Implement this method")

    def delete(self, ctx, payload, resource_id):
        raise NotImplementedError("Please Implement this method")
