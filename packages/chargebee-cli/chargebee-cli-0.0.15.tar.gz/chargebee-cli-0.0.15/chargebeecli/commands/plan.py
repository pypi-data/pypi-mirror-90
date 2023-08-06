from abc import ABC

from chargebeecli.commands.command import Command


class Plan(Command, ABC):
    def get_help_text(self):
        return "Manage plan resource!!!"

    def get_command_name(self):
        return "plan"
