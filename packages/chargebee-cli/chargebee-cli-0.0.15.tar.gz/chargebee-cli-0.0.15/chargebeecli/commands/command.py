import  click
class Command(object, click.Command):
    def get_help_text(self):
        raise NotImplementedError("Please Implement this method")

    def get_command_name(self):
        raise NotImplementedError("Please Implement this method")

    def callback(self):
        pass
