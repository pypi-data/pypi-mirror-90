from typing import List

import importlib

from provider.aws.security.command import SecurityOptions
from provider.aws.security.data.commands_enabled import COMMANDS_ENABLED
from shared.common import (
    ResourceProvider,
    Resource,
    message_handler,
)
from shared.error_handler import exception


def build_formatted_commands():
    formatted_commands = []
    for detail_command in COMMANDS_ENABLED:
        parameters = COMMANDS_ENABLED[detail_command]["parameters"][0]["name"]
        default_value = COMMANDS_ENABLED[detail_command]["parameters"][0][
            "default_value"
        ]
        formated_command = '{}="{}={}"'.format(
            detail_command, parameters, default_value
        )
        formatted_commands.append(formated_command)
    return formatted_commands


class SecuritytResources(ResourceProvider):
    def __init__(self, options: SecurityOptions):
        """
        All resources

        :param options:
        """
        super().__init__()
        self.options = options

    @exception
    # pylint: disable=too-many-locals
    def get_resources(self) -> List[Resource]:

        commands = self.options.commands

        result = []

        # commands informed, checking for specific commands
        if not commands:
            commands = build_formatted_commands()
        # show all commands to check
        if commands[0] == "list":
            message_handler("\nFollowing commands are enabled\n", "HEADER")
            for detail_command in COMMANDS_ENABLED:
                parameters = COMMANDS_ENABLED[detail_command]["parameters"][0]["name"]
                default_value = COMMANDS_ENABLED[detail_command]["parameters"][0][
                    "default_value"
                ]
                description = COMMANDS_ENABLED[detail_command]["short_description"]

                formated_command = 'cloudiscovery aws-security -c {}="{}={}"'.format(
                    detail_command, parameters, default_value
                )
                message_handler(
                    "{} - {} \nExample: {}\n".format(
                        detail_command, description, formated_command
                    ),
                    "OKGREEN",
                )
        else:
            for command in commands:
                command = command.split("=")

                # First position always is command
                if command[0] not in COMMANDS_ENABLED:
                    message_handler(
                        "Command {} doesn't exists.".format(command[0]), "WARNING"
                    )
                else:
                    # Second and thrid parameters are class and method
                    _class = COMMANDS_ENABLED[command[0]]["class"]
                    _method = COMMANDS_ENABLED[command[0]]["method"]
                    _parameter = {
                        command[1].replace('"', ""): command[2].replace('"', "")
                    }

                    module = importlib.import_module(
                        "provider.aws.security.resource.commands." + _class
                    )
                    instance = getattr(module, _class)(self.options)
                    result = result + getattr(instance, _method)(**_parameter)

        return result
