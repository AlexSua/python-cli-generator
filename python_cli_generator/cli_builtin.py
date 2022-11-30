import sys

from enum import Enum
from typing import List
from dataclasses import dataclass

from python_cli_generator import input_processor
from python_cli_generator.output_processor import OutputProcessor


@dataclass
class CliOptions:
    """Options that are going to be applied to the builtin features"""        
    format: str = "json"
    file: str = "output_"+sys.argv[0].replace(".py","")
    configuration_file: str = None
    enable_output_processing: bool = True
    enable_format_argument: bool = True
    enable_file_argument: bool = True
    enable_search_argument: bool = True
    enable_full_help_argument: bool = False
    enable_verbose_argument: bool = True
    enable_attribute_filter_argument: bool = True
    enable_class_attributes_generator: bool = True
    enable_class_functions_generator: bool = True


class FormatOptions(Enum):
    json = "json"
    table = "table"
    raw = "raw"
    csv = "csv"
    yaml = "yaml"


class BuiltinArguments(Enum):
    format = "format"
    file = "file"
    search = "search"
    full_help = "full_help"
    verbose = "verbose"
    attribute_filter = "attribute_filter"


class CliBuiltin:

    _output_processor: OutputProcessor
    cli_options: CliOptions

    def __init__(self,
                 output_processor=None,
                 cli_generator=None,
                 **cli_options: CliOptions):

        self.cli_options = CliOptions()
        self._output_processor = output_processor
        self._cli_generator = cli_generator
        self.cli_options.__dict__.update(cli_options)

        self._builtin_arguments = {
            BuiltinArguments.format: self._generate_format_argument,
            BuiltinArguments.file: self._generate_to_file_argument,
            BuiltinArguments.search: self._generate_search_argument,
            BuiltinArguments.full_help: self._generate_full_help_argument,
            BuiltinArguments.verbose: self._generate_verbose_argument,
            BuiltinArguments.attribute_filter: self._generate_attribute_list_filter_argument,
        }

    def _is_in_sys_argv(self, args):
        if not isinstance(args, list):
            args = [args]
        for arg in args:
            if arg in sys.argv:
                return True
        return False

    def update(self, data: dict):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def _generate_full_help_argument(self, parser, reserved_short_arguments: set[str]):
        short_arg_name = "fh"
        parameter_name = BuiltinArguments.full_help
        doc = "Print all hidden optionals"
        args = ["-"+short_arg_name, "--" +
                short_arg_name, "--"+parameter_name]
        if short_arg_name not in reserved_short_arguments:
            self._cli_generator.create_parameter_argument(
                parser,
                parameter_name=parameter_name,
                parameter_type=bool,
                parameter_default=None,
                parameter_kind=None,
                parameter_doc=doc,
                parameter_destination=parameter_name,
                parameter_metavar=parameter_name,
                reserved_short_arguments=reserved_short_arguments,
                cli_builtin=None,
            )

            if self._is_in_sys_argv(args):
                self.cli_options.enable_full_help_argument = False

    def _generate_verbose_argument(self, parser, reserved_short_arguments: set[str]):
        parameter_name = BuiltinArguments.verbose.value
        doc = "Set the log level to debug"
        self._cli_generator.create_parameter_argument(
            parser,
            parameter_name=parameter_name,
            parameter_type=bool,
            parameter_default=None,
            parameter_kind=None,
            parameter_doc=doc,
            parameter_destination=parameter_name,
            parameter_metavar=parameter_name,
            reserved_short_arguments=reserved_short_arguments,
            cli_builtin=self,
        )

    def _generate_format_argument(self, parser, reserved_short_arguments: set[str]):
        parameter_name = BuiltinArguments.format.value
        doc = "Specify the format that is going to be used as output"
        self._cli_generator.create_parameter_argument(
            parser,
            parameter_name=parameter_name,
            parameter_type=FormatOptions,
            parameter_default=None,
            parameter_kind=None,
            parameter_doc=doc,
            parameter_destination=parameter_name,
            parameter_metavar=parameter_name,
            reserved_short_arguments=reserved_short_arguments,
            cli_builtin=self,
        )

    def _generate_to_file_argument(self, parser, reserved_short_arguments: set[str]):
        parameter_name = BuiltinArguments.file.value
        doc = "Print the result in a file"
        self._cli_generator.create_parameter_argument(
            parser,
            parameter_name=parameter_name,
            parameter_type=str,
            parameter_default=None,
            # parameter_default="output_"+os.path.basename(__file__),
            parameter_kind=None,
            parameter_doc=doc,
            parameter_destination=parameter_name,
            parameter_metavar=parameter_name,
            reserved_short_arguments=reserved_short_arguments,
            cli_builtin=self,
        )

    def _generate_search_argument(self, parser, reserved_short_arguments: set[str]):
        parameter_name = BuiltinArguments.search.value
        doc = "Search inside all values of a list"
        self._cli_generator.create_parameter_argument(
            parser,
            parameter_name=parameter_name,
            parameter_type=str,
            parameter_default=None,
            parameter_kind=None,
            parameter_doc=doc,
            parameter_destination=parameter_name,
            parameter_metavar=parameter_name,
            reserved_short_arguments=reserved_short_arguments,
            cli_builtin=self,
        )

    def _generate_attribute_list_filter_argument(self, parser, reserved_short_arguments: set[str]):
        parameter_name = BuiltinArguments.attribute_filter.value
        doc = "Only print the attributes you select"
        self._cli_generator.create_parameter_argument(
            parser,
            parameter_name=parameter_name,
            parameter_type=List[str],
            parameter_default=None,
            parameter_kind=None,
            parameter_doc=doc,
            parameter_destination=parameter_name,
            parameter_metavar="attribute",
            reserved_short_arguments=reserved_short_arguments,
            cli_builtin=self,
        )
    
    def ask_confirmation(self, message):
        answer = input("{} (\033[37;1my/n\033[0m):".format(message)).lower().strip()
        if answer != "y":
            sys.exit()


    def set_configuration_file(self, cls):
        input_processor.process_configuration_file(cls,self.cli_options.configuration_file)

    def generate_builtin_arguments(self, builtin_arguments_list: list[BuiltinArguments], parser, reserved_short_arguments):
        cli_options = self.cli_options.__dict__
        for arg in builtin_arguments_list:
            enabled_argument = "enable_{}_argument".format(arg.value)
            if enabled_argument in cli_options and cli_options[enabled_argument]:
                self._builtin_arguments[arg](parser, reserved_short_arguments)

    def function_output_decorator(self, func):
        if self.cli_options.enable_output_processing:
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                if self._output_processor:
                    self._output_processor.process_result(result)
                return result
            return wrapper
        return func