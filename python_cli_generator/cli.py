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
    _store = {}
    _reserved_short_arguments: set

    default_command_list_name: str
    function_decorator: FunctionType
    parser: argparse.ArgumentParser
    logger: logging.Logger

    def __init__(self,
                 cli_description: str = None,
                 function_decorator: FunctionType = None,
                 argparser_parser: argparse.ArgumentParser = None,

                 builtin_output_processing: bool = True,
                 builtin_format: str = "json",
                 builtin_search_argument: bool = True,
                 builtin_full_help_argument: bool = False,
                 builtin_verbose_argument: bool = True,
                 builtin_class_attributes_generator: bool = True,
                 builtin_class_functions_generator: bool = True,

                 logger: argparse.ArgumentParser = None,
                 logger_format: str = "\n%(levelname)s : %(asctime)s\
                            \n%(message)s",
                 logger_default_level: int = logging.INFO
                 ):
        """Initialize a CLI instance that contains the necessary information for generating the cli.

        Args:
            cli_description (str, optional): Description of the CLI. Defaults to None.
            function_decorator (FunctionType, optional): Decorator which will wrap the functionality around the function is going to be executed. Defaults to None.
            argparser_parser (argparse.ArgumentParser, optional): Custom argparser parser. If not . Defaults to None.
            builtin_output_processing (bool, optional): Enable the built-in output processor and printer for the result of the executed method. Defaults to True.
            builtin_format (str, optional): Enable the built-in format argument for selecting how the output is going to be displayed on terminal by the output_processor. Defaults to "json".
            builtin_search_argument (bool, optional): Enable the built-in format argument for filtering the output is going to be displayed on terminal by the output_processor. Defaults to True.
            builtin_full_help_argument (bool, optional): Enable the built-in full_help argument for hiding the argparse arguments when the full_help argument is not introduced. Defaults to False.
            builtin_verbose_argument (bool, optional): Enable the built-in argument for showing the logger with the debug level. Defaults to True.
            builtin_class_attributes_generator (bool, optional): Enable/Disable the generation for class attributes. Defaults to True.
            builtin_class_functions_generator (bool, optional): Enable/Disable the generation for class methods. Defaults to True.
            logger (argparse.ArgumentParser, optional): Custom logger that is going to be used by the library. Defaults to None.
            logger_format (str, optional): Default format that is going to be used for printing the log messages. Defaults to "\n%(levelname)s : %(asctime)s\ \n%(message)s".
            logger_default_level (int, optional): The efault logger level. Defaults to logging.INFO.
        """
        super().__init__()
        self.function_decorator = function_decorator
        self.parser = argparser_parser
        self.logger = logger
        self._command = None
        self._args = None
        self._reserved_short_arguments = set()
        self._store= {}
        self.__init_parser(cli_description)
        self.__init_logger(logger_format, logger_default_level)
        self._output_processor = OutputProcessor(self.logger)
        self._cli_generator = CliGenerator(self.function_decorator,self._store)
        self._cli_builtin = CliBuiltin(
            builtin_output_processing,
            builtin_format,
            builtin_search_argument,
            builtin_full_help_argument,
            builtin_verbose_argument,
            builtin_class_attributes_generator,
            builtin_class_functions_generator,
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

    def _generate_arguments_from_dict(self, modules, subparsers=None, subparser_name=None, subparser_doc=None):
        subparsers, _ = self._cli_generator.create_subparser(
            subparsers, subparser_name, doc=subparser_doc)

        for name, item in modules.items():
            self.generate_arguments(
                item, subparsers=subparsers, subparser_name=name, subparser_doc=subparser_doc
            )

    def _generate_arguments_from_tuple(self,  input, subparsers, subparser_name=None, subparser_doc=None, **options):
        value = input[0]
        options = input[1] if len(input) > 1 else {}
        if isinstance(options, str):
            subparser_doc = options
            options = {}
        options = {"subparser_name": subparser_name,
                   "subparser_doc": subparser_doc, **options, }
        self.generate_arguments(
            value, subparsers=subparsers, **options)

    def _generate_arguments_from_class(self, input, subparsers, subparser_name=None,
                                       reserved_short_arguments=None, **options):
        cli_builtin = copy.copy(self._cli_builtin)
        cli_builtin.update(options)
        self._cli_generator.generate_arguments_from_class(
            subparsers, input, cli_builtin, subparser_name=subparser_name,
            reserved_short_arguments=reserved_short_arguments,
        )
        self._class_instances.append(input)

    def _generate_arguments_from_function(self, input, subparsers, subparser_name=None,
                                          reserved_short_arguments=None, **options):
        cli_builtin = copy.copy(self._cli_builtin)
        cli_builtin.update(options)
        self._cli_generator.generate_arguments_from_function(
            subparsers, input, cli_builtin, subparser_name=subparser_name,
            reserved_short_arguments=reserved_short_arguments
        )

    def _generate_arguments_from_list(self, list, subparsers=None, subparser_name=None, **options):

        subparsers, _ = self._cli_generator.create_subparser(
            subparsers, subparser_name, add_subparsers=False)
        reserved_short_arguments = set()        
        for input_array_element in list:
            self.generate_arguments(input_array_element, subparsers=subparsers,
                                    reserved_short_arguments=reserved_short_arguments)

    def generate_arguments(self, input, subparsers=None, **options):
        """Generate argparse arguments from the inserted input.

        Args:
            input (Class, dict, List): Introduce the class, dictionary (see the documentation) or list of elements from which the library generates the code.
            subparsers (argparse.ArgumentParser, optional): Subparsers . Defaults to None.
            builtin_output_processing (bool, optional): Enable the built-in output processor and printer for the result of the executed method. Defaults to True.
            builtin_format (str, optional): Enable the built-in format argument for selecting how the output is going to be displayed on terminal by the output_processor. Defaults to "json".
            builtin_search_argument (bool, optional): Enable the built-in format argument for filtering the output is going to be displayed on terminal by the output_processor. Defaults to True.
            builtin_full_help_argument (bool, optional): Enable the built-in full_help argument for hiding the argparse arguments when the full_help argument is not introduced. Defaults to False.
            builtin_verbose_argument (bool, optional): Enable the built-in argument for showing the logger with the debug level. Defaults to True.
            builtin_class_attributes_generator (bool, optional): Enable/Disable the generation for class attributes. Defaults to True.
            builtin_class_functions_generator (bool, optional): Enable/Disable the generation for class methods. Defaults to True.
            subparser_name (str, optional): Name of the subcommand. Defaults to None.
            subparser_doc (str, optional): Documentation for the current subcommand. Defaults to None.
        """        
        if subparsers is None:
            subparsers = self.parser

        instance_dict = {
            tuple: self._generate_arguments_from_tuple,
            dict: self._generate_arguments_from_dict,
            list: self._generate_arguments_from_list,
            FunctionType: self._generate_arguments_from_function,
            object: self._generate_arguments_from_class
        }

        for input_type in instance_dict:
            if isinstance(input, input_type):
                instance_dict[input_type](input, subparsers, **options)
                break

    def parse(self):
        """Parse the arguments that were generated using the method "generate_arguments".
        """
        args = self.parser.parse_args()
        self._command = args.func
        args = parsing_processor.process_parsed_arguments(args,self._store)
        self._output_processor.process_args(args)
        for class_instance in self._class_instances:
            parsing_processor.set_args_into_class(args, class_instance)
        self._args = args
        return args

    def execute_command(self):
        """Execute the selected command.
        """
        func_args = self._args.get("func_args", {})
        return self._command(**func_args)
