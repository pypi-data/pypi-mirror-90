import click


class Command(object):
    def get_help_text(self):
        raise NotImplementedError("Please Implement this method")

    def get_command_name(self):
        raise NotImplementedError("Please Implement this method")

    def callback(self):
        pass

    def get_options(self):
        raise NotImplementedError("Please Implement this method")

    def get_arguments(self):
        raise NotImplementedError("Please Implement this method")
