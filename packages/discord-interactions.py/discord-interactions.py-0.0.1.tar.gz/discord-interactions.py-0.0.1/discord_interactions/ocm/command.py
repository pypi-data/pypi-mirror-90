from discord_interactions import (
    Interaction, Member, ApplicationCommandInteractionDataOption,
    ApplicationCommand, ApplicationCommandOption, ApplicationCommandOptionType, ApplicationCommandOptionChoice
)
from typing import List, Union
from dataclasses import dataclass
from enum import Enum


class OptionChoices(Enum):
    @classmethod
    def to_application_command_option_choices(cls) -> List[ApplicationCommandOptionChoice]:
        choices = []

        for choice in cls:
            choices.append(ApplicationCommandOptionChoice(choice.name, choice.value))

        return choices


class _Option:
    pass


class OptionContainerType(type):
    def __new__(mcs, name, bases, attributes):
        cls = super(OptionContainerType, mcs).__new__(mcs, name, bases, attributes)

        for attr_name, attr in attributes.items():
            if isinstance(attr, _Option):
                # set option name to attribute name where not explicitly set
                if attr.name is None:
                    attr.name = attr_name

                # set option type based on type annotations where not explicitly set
                if attr.type is None:
                    attr.type = ApplicationCommandOptionType.STRING  # use string as default option type
                    if cls.__annotations__:
                        _type = cls.__annotations__.get(attr_name)
                        if isinstance(_type, ApplicationCommandOptionType):
                            attr.type = _type
                        elif _type == int:
                            attr.type = ApplicationCommandOptionType.INTEGER

        return cls


@dataclass()
class Option(_Option, metaclass=OptionContainerType):
    description: str
    type: ApplicationCommandOptionType = None
    name: str = None
    default: bool = False
    required: bool = False
    choices: OptionChoices = None
    __data: ApplicationCommandInteractionDataOption = None
    __data_loaded: bool = False

    @property
    def is_sub_command(self):
        return self.type in (
            ApplicationCommandOptionType.SUB_COMMAND,
            ApplicationCommandOptionType.SUB_COMMAND_GROUP
        )

    def __get__(self, instance: Union["Command", "Option"], owner):
        if not self.is_sub_command:
            data = getattr(instance, "_Command__interaction").data if not isinstance(self, owner) else instance.__data
            return data.get_option(self.name)

        if not self.__data_loaded:
            if isinstance(self, owner):
                self.__data = instance.__data.get_option(self.name)
            else:
                self.__data = getattr(instance, "_Command__interaction").data.get_option(self.name)
            self.__data_loaded = True
        return self.__data

    def to_application_command_option(self) -> ApplicationCommandOption:
        options = []
        for option in self.__dict__.values():
            if not isinstance(option, Option):
                continue
            options.append(option.to_application_command_option())

        if self.choices:
            choices = self.choices.to_application_command_option_choices()
        else:
            choices = None

        return ApplicationCommandOption(
            type=self.type,
            name=self.name,
            description=self.description,
            default=self.default,
            required=self.required,
            options=options or None,
            choices=choices
        )


class CommandType(OptionContainerType):
    def __new__(mcs, *args, **kwargs):
        cls = super(CommandType, mcs).__new__(mcs, *args, **kwargs)

        # abort if it's a class in this module (the `Command` class itself and not a subclass)
        if cls.__module__ == __name__:
            return cls

        if cls.__cmd_name__ is None:
            cls.__cmd_name__ = cls.__name__.lower().strip("_")

        if cls.__cmd_description__ is None and cls.__doc__ is not None:
            cls.__cmd_description__ = cls.__doc__.strip()

        return cls


class Command(metaclass=CommandType):
    """ Represents a Discord Slash Command in the Object-Command-Mapper (OCM). """

    __cmd_name__ = None
    __cmd_description__ = None

    __interaction: Interaction = None

    @classmethod
    def wrap(cls, interaction: Interaction):
        inst = cls()
        inst.__interaction = interaction
        # inst.__wrap_options__(interaction.data.options)
        return inst

    @property
    def guild_id(self) -> int:
        return self.__interaction.guild_id

    @property
    def channel_id(self) -> int:
        return self.__interaction.channel_id

    @property
    def member(self) -> Member:
        return self.__interaction.member

    @property
    def interaction_id(self) -> int:
        return self.__interaction.id

    @property
    def command_id(self) -> int:
        return self.__interaction.data.id

    @classmethod
    def to_application_command(cls) -> ApplicationCommand:
        options = []

        for option in cls.__dict__.values():
            if not isinstance(option, Option):
                continue
            options.append(option.to_application_command_option())

        return ApplicationCommand(
            name=cls.__cmd_name__,
            description=cls.__cmd_description__,
            options=options or None
        )
