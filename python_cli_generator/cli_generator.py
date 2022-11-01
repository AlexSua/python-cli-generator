import argparse
import copy
import inspect
import json
from logging import exception
import sys

from enum import Enum
from datetime import datetime
from types import FunctionType
from typing import Any, List, Type, get_type_hints

from python_cli_generator.cli_builtin import CliBuiltin
from python_cli_generator.parsing_processor import validate_json


class CliGenerator:

    def __init__(self, func_decorator: FunctionType = None, store:dict=None):
        self.func_decorator = func_decorator
        self._store = store

    def _save_in_store(self,key,value):
        if self._store is not None:
            self._store[key] = value

    def _generate_short_argument(self, parameter_name: str, reserved_short_arguments: set[str]):
        parameter_name_underscores = parameter_name.replace(".", "_")
        splitted = parameter_name_underscores.split("_")
        counter = [0]*len(splitted)
        max_size = [len(split) for split in splitted]
        while (True):
            arg_key = ""
            for i, split in enumerate(splitted):
                arg_key = arg_key + split[0:counter[i]+1]
                arg_key = arg_key.lower()

            if arg_key not in reserved_short_arguments:
                reserved_short_arguments.add(arg_key)
                return arg_key

            else:
                cancounter = False
                for j, countj in enumerate(counter):
                    countjok = False
                    if counter[j] < max_size[j]:
                        for k, countk in enumerate(counter, j+1):
                            if countk >= countj:
                                countjok = True
                                break
                        if countjok:
                            counter[j] += 1
                            cancounter = True
                            break

                if not cancounter:
                    parameter_name_join = parameter_name_underscores.replace(
                        "_", ".")
                    ic = 0
                    while (True):
                        arg_key = arg_key + \
                            parameter_name_join[ic % len(parameter_name_join)]
                        arg_key = arg_key.lower()
                        if arg_key not in reserved_short_arguments:
                            reserved_short_arguments.add(arg_key)
                            return arg_key

    def _process_enum(self, arguments, parameter_type, parameter_default=None):
        def __str__(cls):
            return str(cls.value)
        choices_parameter = parameter_type
        if parameter_default != None:
            choices_parameter = parameter_default.__class__
        setattr(choices_parameter, "__str__", __str__)
        arguments[1]["choices"] = list(choices_parameter)
        if "metavar" in arguments[1]: del arguments[1]["metavar"]

    def _process_datetime(self, arguments, parameter_default):
        # if parameter_default == None:
        def _datetime_function(s):
            try:
                return datetime.strptime(s,"%Y-%m-%d")
            except Exception:
                return datetime.strptime(s,"%Y-%m-%d/%H:%M:%S")
            
        arguments[1]["type"] = _datetime_function

    def _process_optional(self, arguments, parameter_metavar, parameter_default, reserved_short_arguments):
        arg_key = self._generate_short_argument(
            parameter_metavar, reserved_short_arguments)

        arguments[0].append("-" + arg_key)
        arguments[0].append("--" + arg_key)
        arguments[0].append("--" + parameter_metavar)

        arguments[1]["default"] = parameter_default

    def _process_list(self, arguments, parameter_type):
        arguments[1]["nargs"] = "+"
        arguments[1]["type"] = parameter_type.__args__[0]
        if parameter_type.__args__[0].__module__ != "builtins":
            def argparse_func(value):
                value = json.loads(value)
                result = validate_json(value, parameter_type.__args__[0])
                if not result:
                    raise ValueError(
                        "The introduced json doesn't have the proper format.")
                return value

            arguments[1]["type"] = argparse_func

    def _process_subtype(self, arguments, parameter_type):
        arguments[1]["type"] = parameter_type.__args__[0]

    def _process_class(self, arguments, parameter_type: Type, parameter_name: str, parameter_default, parameter_kind,  **options):
        arguments[1]["metavar"] = parameter_name

        self.generate_arguments_from_class(
            class_instance=parameter_default if parameter_default is not None and parameter_default is not inspect._empty else parameter_type,
            # subparser_name= parameter_name if parameter_kind is not None else None,
            parameter_kind=parameter_kind,
            **options
        )

    def _process_no_type(self, arguments, parameter_type):
        parameter_type = str
        arguments[1]["type"] = parameter_type

    def _process_bool(self, arguments):
        arguments[1]["action"] = "store_true"
        del arguments[1]["type"]
        del arguments[1]["metavar"]

    def _process_help(self, arguments, builtin_full_help_argument=False):
        if builtin_full_help_argument:
            arguments[1]["help"] = argparse.SUPPRESS

    def _print_argparse_arguments(self, arguments):
        initial_parameters = arguments[1]
        st = ""
        for initial_parameters in initial_parameters:
            st += '"' + initial_parameters + '",'
        for argument in arguments:
            if argument == "help":
                st += argument + '="' + str(arguments[argument]) + '",'
                continue
            if argument == "type":
                st += argument + "=" + arguments[argument].__name__ + ","
                continue
            st += argument + '="' + str(arguments[argument]) + '",'
        st = st[:-1]
        print("parser.add_argument({})".format(st))

    def _is_arg_in_args(self,arg:str):
        if arg is not None and arg not in sys.argv:
            return False
        else:
            return True

    def create_subparser(self, parser, subparser_name=None, doc=None, add_subparsers=True):
        subparsers = None
        if hasattr(parser, "_subparsers") and parser._subparsers is None:
            subparsers = parser.add_subparsers(
                help=doc,
            )
            setattr(parser, "subparsers", subparsers)
        else:
            subparsers = parser.subparsers

        if subparser_name is not None:
            parser = subparsers.add_parser(
                subparser_name, help=doc, allow_abbrev=False)
            parser.set_defaults(func=parser.print_help, allow_abbrev=False)
            if add_subparsers:
                subparsers = parser.add_subparsers()
            setattr(parser, "subparsers", subparsers)

        return (parser, subparsers)

    def create_parameter_argument(
        self,
        parser,
        parameter_name: str,
        parameter_default: Any,
        parameter_kind: Any,
        parameter_type: Type = str,
        parameter_doc: str = None,
        parameter_destination: str = "",
        parameter_metavar: str = None,
        reserved_short_arguments: set[str] = None,
        print_argparse_code: bool = False,
        builtin_options: CliBuiltin = None
    ):
        arguments = (
            [], {
                "type": parameter_type,
                "dest": parameter_destination,
                "metavar": parameter_metavar if parameter_metavar is not None else parameter_name,
                "help": parameter_doc,
            }
        )

        if parameter_type is inspect._empty:
            self._process_no_type(arguments, parameter_type)
            parameter_type = arguments[1]["type"]

        if builtin_options is None:
            builtin_options = CliBuiltin()

        if reserved_short_arguments is None:
            reserved_short_arguments = set()

        if parameter_default is not inspect._empty:
            self._process_optional(
                arguments, parameter_metavar, parameter_default, reserved_short_arguments)

        if hasattr(parameter_type, "__args__") and (
            len(parameter_type.__args__) == 2 and parameter_type.__args__[
                -1] is type(None)
        ):
            self._process_subtype(arguments, parameter_type)
            parameter_type = arguments[1]["type"]

        if (hasattr(parameter_type, "_gorg") and parameter_type._gorg == List) or (
            hasattr(parameter_type, "_name") and parameter_type._name == "List"
        ):
            self._process_list(arguments, parameter_type)
            parameter_type = arguments[1]["type"]

        if inspect.isclass(parameter_type):

            if issubclass(parameter_type, Enum) or parameter_type == Enum or parameter_type.__name__ == "EnumMeta":
                self._process_enum(arguments, parameter_type=parameter_type)

            elif issubclass(parameter_type, datetime) or parameter_type == datetime:
                self._process_datetime(
                    arguments, parameter_default)
                parameter_type = arguments[1]["type"]

            elif parameter_type.__module__ != "builtins":
                self._process_class(arguments, parameter_type, parameter_name, parameter_default, parameter_kind, destination_name=parameter_destination, parser=parser,
                                    reserved_short_arguments=reserved_short_arguments, builtin_options=builtin_options)
                return

        if parameter_type == bool:
            self._process_bool(arguments)

        self._process_help(
            arguments, builtin_full_help_argument=builtin_options.builtin_full_help_argument)

        if callable(parameter_type):
            if print_argparse_code:
                self._print_argparse_arguments(arguments)
            parser.add_argument(*arguments[0], **arguments[1])

    def generate_arguments_from_function(self, parser, function, builtin_options=None, reserved_short_arguments=None, subparser_name=None, parameter_destination="func_args.", is_constructor=False):
        doc = function.__doc__
        function_doc = doc.split("\n")[0] if doc is not None else doc

        if subparser_name is not None:
            parser, _ = self.create_subparser(
                parser, subparser_name, function_doc)

        if not self._is_arg_in_args(subparser_name): return

        if builtin_options is None:
            builtin_options = CliBuiltin()
        else:
            builtin_options = copy.copy(builtin_options)

        builtin_options.builtin_full_help_argument = False

        if not is_constructor:
            parser_function = function

            if self.func_decorator:
                parser_function = self.func_decorator(function)

            if builtin_options.builtin_output_processing:
                parser_function = builtin_options.function_output_decorator(
                    function)

            parser.set_defaults(func=parser_function)
            builtin_options.generate_format_argument(
                parser, reserved_short_arguments)
            builtin_options.generate_verbose_argument(
                parser, reserved_short_arguments)
            builtin_options.generate_search_argument(
                parser, reserved_short_arguments)
            builtin_options.generate_attribute_list_filter_argument(
                parser, reserved_short_arguments)

        signature = inspect.signature(function)

        for parameter in signature.parameters:
            parameter_value = signature.parameters[parameter]
            if (parameter == "self"
                or (is_constructor and parameter == "args" and parameter_value.VAR_KEYWORD == 4)
                    or (is_constructor and parameter == "kwargs" and parameter_value.VAR_KEYWORD == 4)):
                continue

            if doc is not None:
                docArr = function.__doc__.split(
                    "    " + parameter + " ", 1)
                if len(docArr) > 1:
                    doc = docArr[1].split("\n")[0]
                else:
                    doc = None

            self.create_parameter_argument(
                parser,
                parameter_name=parameter,
                parameter_type=parameter_value.annotation,
                parameter_default=parameter_value.default,
                parameter_kind=parameter_value.kind,
                parameter_doc=doc,
                parameter_destination=parameter_destination+parameter,
                parameter_metavar=parameter,
                reserved_short_arguments=reserved_short_arguments,
                builtin_options=builtin_options,
            )

    def generate_arguments_from_class(
        self,
        parser,
        class_instance,
        builtin_options=None,
        destination_name: str = None,
        subparser_name: str = None,
        member_list_allowed: List[str] = None,
        reserved_short_arguments: set[str] = None,
        parameter_kind: inspect._ParameterKind = None
    ):

        if builtin_options is None:
            builtin_options = CliBuiltin()

        if reserved_short_arguments is None:
            reserved_short_arguments = set()

        class_doc = class_instance.__doc__.split(
            "\n")[0] if class_instance.__doc__ else None

        DEFAULT_METHOD_NAME = "_default"
        has_default_method = hasattr(class_instance, DEFAULT_METHOD_NAME)

        if builtin_options.builtin_class_functions_generator and parameter_kind is None:
            parser, subparsers = self.create_subparser(parser, subparser_name, class_doc,
                                                       add_subparsers=not has_default_method and builtin_options.builtin_class_functions_generator,
                                                       )

        if not self._is_arg_in_args(subparser_name): return

        if destination_name is None:
            if not class_instance.__class__.__name__ == "type":
                destination_name = class_instance.__class__.__name__
            else:
                destination_name = class_instance.__name__

        functionParameter = False
        if parameter_kind is not None:
            functionParameter = True
            if parameter_kind is not inspect._ParameterKind.VAR_KEYWORD:
                parameter_class_name = class_instance.__name__
                self._save_in_store(parameter_class_name,class_instance)
                parameter_constructor_destination = destination_name + "."+"$constructor_{}.".format(parameter_class_name)
                self.generate_arguments_from_function(parser, class_instance.__init__, builtin_options, reserved_short_arguments,
                                                      parameter_destination=parameter_constructor_destination, is_constructor=True)
                # parser, subparsers  = self.create_subparser(parser,subparser_name, add_subparsers=False,parameter_destination= )
                parameter_kind = inspect._ParameterKind.VAR_KEYWORD

        builtin_options.generate_full_help_argument(
            parser, reserved_short_arguments)

        class_members_list = inspect.getmembers(
            class_instance)

        class_hints = {}

        if not class_instance.__class__.__name__ == "type":
            try:
                class_hints = get_type_hints(class_instance)
            except Exception:
                pass

        for class_hint, _ in class_hints.items():
            if not hasattr(class_instance, class_hint):
                class_members_list.append(
                    (class_hint, inspect._empty if parameter_kind else None))

        for member_name, member in class_members_list:
            if (
                (member_list_allowed != None and member_name not in member_list_allowed)
                or (member_name.startswith("_") and member_name != DEFAULT_METHOD_NAME)
            ):
                continue

            doc = None

            if member.__doc__ is not None:
                doc = member.__doc__.split("\n")[0]

            parameter_destination = destination_name + "." + member_name

            parameter_metavar = parameter_destination.split(".", 1)
            if len(parameter_metavar) > 1:
                parameter_metavar = parameter_metavar[1]
            else:
                parameter_metavar = parameter_metavar[0]

            if (inspect.ismethod(member) or inspect.isfunction(member)) and not functionParameter:
                if builtin_options.builtin_class_functions_generator:
                    reserved_short_arguments_per_method = copy.copy(
                        reserved_short_arguments)

                    function_subparser = parser
                    if not has_default_method:
                        function_subparser = subparsers.add_parser(
                            parameter_metavar, help=doc, allow_abbrev=False)
                    self.generate_arguments_from_function(
                        function_subparser, member, builtin_options=builtin_options, reserved_short_arguments=reserved_short_arguments_per_method)

            else:
                if builtin_options.builtin_class_attributes_generator:
                    doc = class_instance.__doc__
                    if doc is not None:
                        docArr = doc.split(
                            "    " +
                            member_name.split(".")[-1] + " ", 1
                        )
                        if len(docArr) > 1:
                            doc = docArr[1].split("\n")[0]
                        else:
                            doc = None

                self.create_parameter_argument(
                    parser,
                    parameter_name=member_name,
                    parameter_type=class_hints[member_name] if member_name in class_hints else member.__class__,
                    parameter_default=member,
                    parameter_kind=parameter_kind,
                    parameter_doc=doc,
                    parameter_destination=parameter_destination,
                    parameter_metavar=parameter_metavar,
                    reserved_short_arguments=reserved_short_arguments,
                    builtin_options=builtin_options
                )
