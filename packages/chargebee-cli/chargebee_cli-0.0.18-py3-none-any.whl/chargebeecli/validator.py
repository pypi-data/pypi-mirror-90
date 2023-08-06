from chargebeecli.util.printer import custom_print_error


class Validator(object):

    def validate_param(self, __input_columns):
        raise NotImplementedError("Please Implement this method")

    def validate_param(self, __input_columns, headers):
        if __input_columns is not None and len(__input_columns) > 0:
            for column in __input_columns:
                if column not in headers:
                    custom_print_error(f"Unknown column :{column}")
                    exit()
            headers = __input_columns
        return headers

    def validate_ids(self, __input_columns, headers):
        if __input_columns is not None and len(__input_columns) > 0:
            for column in __input_columns:
                if column not in headers:
                    custom_print_error(f"Unknown column :{column}")
                    exit()
            headers = __input_columns
        return headers
