import sys
from enum import Enum
from typing import List

from python_cli_generator.output_processor import OutputProcessor


class FormatOptions(Enum):
    json = "json"
    table = "table"
    raw = "raw"


class CliBuiltin:

    builtin_output_processing: bool
    builtin_format: str
    builtin_search_argument: bool
    builtin_full_help_argument: bool
    builtin_verbose_argument: bool
    _output_processor: OutputProcessor

    def __init__(self, builtin_output_processing: bool = True,
                 builtin_format: str = "json",
                 builtin_search_argument: bool = True,
                 builtin_full_help_argument: bool = False,
                 builtin_verbose_argument: bool = True,
                 builtin_class_attributes_generator:bool = True,
                 builtin_class_functions_generator:bool=True,
                 output_processor=None,
                 cli_generator=None):

        self.builtin_output_processing = builtin_output_processing
        self.builtin_format = builtin_format
        self.builtin_search_argument = builtin_search_argument
        self.builtin_full_help_argument = builtin_full_help_argument
        self.builtin_verbose_argument = builtin_verbose_argument
        self.builtin_class_attributes_generator = builtin_class_attributes_generator
        self.builtin_class_functions_generator = builtin_class_functions_generator

        self._output_processor = output_processor
        self._cli_generator = cli_generator

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

    def generate_full_help_argument(self, parser, reserved_short_arguments: set[str]):
        if self.builtin_full_help_argument:
            short_arg_name = "fh"
            parameter_name = "full_help"
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
                    builtin_options=None,
                )

                if self._is_in_sys_argv(args):
                    self.builtin_full_help_argument = False

    def generate_verbose_argument(self, parser, reserved_short_arguments: set[str]):
        parameter_name = "verbose"
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
            builtin_options=self,
        )

    def generate_format_argument(self, parser, reserved_short_arguments: set[str]):
        parameter_name = "format"
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
            builtin_options=self,
        )

    def generate_search_argument(self, parser, reserved_short_arguments: set[str]):
        parameter_name = "search"
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
            builtin_options=self,
        )

    def generate_attribute_list_filter_argument(self, parser, reserved_short_arguments: set[str]):
        parameter_name = "attributes"
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
            builtin_options=self,
        )

    def function_output_decorator(self, func):
        if self.builtin_output_processing:
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                if self._output_processor:
                    self._output_processor.process_result(result)
                return result
            return wrapper
        return func