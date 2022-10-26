import copy
import argparse
import logging
from types import FunctionType

from python_cli_generator.cli_builtin import CliBuiltin
from python_cli_generator.cli_generator import CliGenerator
from python_cli_generator.output_processor import OutputProcessor
import python_cli_generator.parsing_processor as parsing_processor

class Cli():
    _class_instances = []

    default_command_list_name: str
    function_decorator: FunctionType
    parser: argparse.ArgumentParser

    logger: logging.Logger

    def __init__(self,
                 cli_description: str = None,
                 default_command_list_name: str = None,
                 function_decorator: FunctionType = None,
                 argparser_parser: argparse.ArgumentParser = None,

                 builtin_output_processing: bool = True,
                 builtin_format: str = "json",
                 builtin_search_argument: bool = True,
                 builtin_full_help_argument: bool = False,
                 builtin_verbose_argument: bool = True,

                 logger: argparse.ArgumentParser = None,
                 logger_format: str = "\n%(levelname)s : %(asctime)s\
                            \n%(message)s",
                 logger_default_level: int = logging.INFO
                 ):

        super().__init__()
        self.function_decorator = function_decorator
        self.default_command_list_name = default_command_list_name
        self.parser = argparser_parser
        self.logger = logger
        self._command = None
        self._args = None
        self.__init_parser(cli_description)
        self.__init_logger(logger_format, logger_default_level)
        self._output_processor = OutputProcessor(self.logger)
        self._cli_generator = CliGenerator(self.function_decorator)
        self._cli_builtin = CliBuiltin(
            builtin_output_processing,
            builtin_format,
            builtin_search_argument,
            builtin_full_help_argument,
            builtin_verbose_argument,
            logger=logger,
            output_processor=self._output_processor,
            cli_generator=self._cli_generator
        )

    def __init_parser(self, cli_description: str):
        if self.parser is None:
            self.parser = argparse.ArgumentParser(
                allow_abbrev=False,
                formatter_class=argparse.HelpFormatter,
                description=cli_description,
            )
            self.parser.set_defaults(func=self.parser.print_help)

    def __init_logger(self, logger_format: str, logger_default_level: int):
        if self.logger is None:
            logging.basicConfig(
                format=logger_format,
            )
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logger_default_level)

    def _generate_arguments_from_modules(self, modules, subparsers=None, subparser_name=None, subparser_doc=None):
        subparsers, _ = self._cli_generator.create_subparser(
            subparsers, subparser_name, doc=subparser_doc)
        for name, item in modules.items():
            if isinstance(item, tuple):
                value = item[0]
                options = item[1] if len(item)>1 else {}
                if isinstance(options,str):
                    subparser_doc = options
                    options = {}
                self.generate_arguments(
                    value, subparsers=subparsers, subparser_name=name,  subparser_doc = subparser_doc, **options
                )
            else:
                self.generate_arguments(
                    item, subparsers=subparsers, subparser_name=name, subparser_doc = subparser_doc
                )

    def _generate_arguments_from_class(self, input, subparsers, subparser_name, **options):
        cli_builtin = copy.copy(self._cli_builtin)
        cli_builtin.update(options)
        self._cli_generator.generate_arguments_from_class(
            subparsers, input, cli_builtin, subparser_name=subparser_name,
        )
        self._class_instances.append(input)

    def _generate_arguments_from_function(self, input, subparsers, subparser_name, **options):
        cli_builtin = copy.copy(self._cli_builtin)
        cli_builtin.update(options)
        self._cli_generator.generate_arguments_from_function(
            subparsers, input, cli_builtin, subparser_name=subparser_name,
        )

    def _generate_arguments_from_list(self, list, subparsers=None, subparser_name=None, **options):
        subparsers, _ = self._cli_generator.create_subparser(
            subparsers, subparser_name)
        for input_array_element in list:
            self.generate_arguments(input_array_element, subparsers=subparsers)

    def generate_arguments(self, input, subparsers=None, subparser_name=None, **options):
        if subparsers is None:
            subparsers = self.parser

        if isinstance(input, dict):
            self._generate_arguments_from_modules(
                input, subparsers, subparser_name, **options)

        elif isinstance(input, list):
            self._generate_arguments_from_list(
                input, subparsers, subparser_name, **options)

        elif isinstance(input, FunctionType):
            self._generate_arguments_from_function(
                input, subparsers, subparser_name, **options)

        elif isinstance(input, object):
            self._generate_arguments_from_class(
                input, subparsers, subparser_name, **options)

    def parse(self):
        args = self.parser.parse_args()
        self._command = args.func
        args = parsing_processor.process_parsed_arguments(args)
        self._output_processor.process_args(args)
        for class_instance in self._class_instances:
            parsing_processor.set_args_into_class(args, class_instance)
        self._args = args
        return args

    def execute_command(self):
        func_args = self._args.get("func_args", {})
        return self._command(**func_args)
