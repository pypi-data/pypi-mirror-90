# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Argufy is an inspection based CLI parser.'''

import inspect
import logging
import sys
from argparse import ArgumentParser, Namespace, _SubParsersAction
from inspect import _ParameterKind
from types import ModuleType
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
)

from docstring_parser import parse

from .argument import Argument
from .formatter import ArgufyHelpFormatter

log = logging.getLogger(__name__)

# Define function as parameters for MyPy
F = TypeVar('F', bound=Callable[..., Any])


class Parser(ArgumentParser):
    '''Provide CLI parser for function.'''

    exclude_prefixes = ('@', '_')

    def __init__(self, *args: str, **kwargs: str) -> None:
        '''Initialize parser.

        Parameters
        ----------
        prog: str
            The name of the program
        usage: str
            The string describing the program usage
        description: str
            Text to display before the argument help
        epilog: str
            Text to display after the argument help
        parents: list
            A list of ArgumentParser objects whose arguments should also
            be included
        formatter_class: Object
            A class for customizing the help output
        prefix_chars: char
            The set of characters that prefix optional arguments
        fromfile_prefix_chars: None
            The set of characters that prefix files from which additional
            arguments should be read
        argument_default: None
            The global default value for arguments
        conflict_handler: Object
            The strategy for resolving conflicting optionals
        add_help: str
            Add a -h/--help option to the parser
        allow_abbrev: bool
            Allows long options to be abbreviated if the abbreviation is
            unambiguous

        '''
        # TODO: handle environment variables

        module = self.__get_parent_module()
        if module:
            docstring = parse(module.__doc__)
            if not kwargs.get('description'):
                kwargs['description'] = docstring.short_description

            if 'prog' not in kwargs:
                kwargs['prog'] = module.__name__.split('.')[0]

        # if 'prefix' in kwargs:
        #     self.prefix = kwargs.pop('prefix')
        # else:
        #     self.prefix = kwargs['prog'].upper()
        # log.debug(self.prefix)

        if 'formatter_class' not in kwargs:
            self.formatter_class = ArgufyHelpFormatter

        if 'log_level' in kwargs:
            log.setLevel(getattr(logging, kwargs.pop('log_level').upper()))
        if 'log_handler' in kwargs:
            log_handler = kwargs.pop('log_handler')
            log.addHandler(logging.StreamHandler(log_handler))  # type: ignore

        if 'version' in kwargs:
            self.prog_version = kwargs.pop('version')

        self.command_type = kwargs.pop('command_type', None)
        self.command_scheme = kwargs.pop('command_scheme', None)

        super().__init__(**kwargs)  # type: ignore

        # NOTE: cannot move to formatter
        self._positionals.title = ArgufyHelpFormatter.font(
            self._positionals.title or 'arguments'
        )
        self._optionals.title = ArgufyHelpFormatter.font(
            self._optionals.title or 'flags'
        )

        if hasattr(self, 'prog_version'):
            self.add_argument(
                '--version',
                action='version',
                version=f"%(prog)s {self.prog_version}",
                help='display package version',
            )

    @staticmethod
    def __get_parent_module() -> Optional[ModuleType]:
        '''Get parent name importing this module.'''
        stack = inspect.stack()
        # TODO: need way to better identify parent module
        stack_frame = stack[2]
        result = inspect.getmodule(stack_frame[0]) or None
        return result

    @staticmethod
    def __get_args(argument: Argument) -> Dict[Any, Any]:
        '''Retrieve arguments from Argument.'''
        return {
            k[len('_Argument__') :]: v  # noqa
            for k, v in vars(argument).items()
            if k.startswith('_Argument__')
        }

    @staticmethod
    def _get_excludes(exclude_prefixes: tuple = tuple()) -> tuple:
        '''Combine class excludes with instance.'''
        if exclude_prefixes != []:
            return tuple(exclude_prefixes) + Parser.exclude_prefixes
        else:
            return Parser.exclude_prefixes

    def add_arguments(
        self, obj: Any, parser: Optional[ArgumentParser] = None
    ) -> 'Parser':
        '''Add arguments to parser/subparser.'''
        if not parser:
            parser = self
        docstring = parse(obj.__doc__)
        signature = inspect.signature(obj)
        for arg in signature.parameters:
            description = next(
                (d for d in docstring.params if d.arg_name == arg), None,
            )
            arguments = self.__get_args(
                Argument(signature.parameters[arg], description)
            )
            log.debug(f"arguments {arguments}")
            name = arguments.pop('name')
            parser.add_argument(*name, **arguments)
        return self

    def add_commands(
        self,
        module: ModuleType,
        parser: Optional[ArgumentParser] = None,
        exclude_prefixes: tuple = tuple(),
        command_type: Optional[str] = None,
    ) -> 'Parser':
        '''Add commands.'''
        module_name = module.__name__.split('.')[-1]
        docstring = parse(module.__doc__)

        # use self or an existing parser
        if not parser:
            parser = self

        # use exsiting subparser or create a new one
        if not any(isinstance(x, _SubParsersAction) for x in parser._actions):
            parser.add_subparsers(dest=module_name, parser_class=Parser)

        # check if command exists
        command = next(
            (x for x in parser._actions if isinstance(x, _SubParsersAction)),
            None,
        )
        excludes = Parser._get_excludes(exclude_prefixes)

        # set command name scheme
        if command_type is None:
            command_type = self.command_type

        # create subcommand for command
        if command_type == 'subcommand':
            if command:
                msg = docstring.short_description
                subcommand = command.add_parser(
                    module_name.replace('_', '-'),
                    description=msg,
                    formatter_class=ArgufyHelpFormatter,
                    help=msg,
                )
                subcommand.set_defaults(mod=module)
                parser.formatter_class = ArgufyHelpFormatter

            # append subcommand to exsiting command or create a new one
            return self.add_commands(
                module=module,
                parser=subcommand,
                exclude_prefixes=Parser._get_excludes(exclude_prefixes),
                command_type='command',
            )

        for name, value in inspect.getmembers(module):
            # TODO: Possible singledispatch candidate
            if not name.startswith(excludes):
                # skip classes for now
                if inspect.isclass(value):
                    continue  # pragma: no cover

                # create commands from functions
                elif inspect.isfunction(value):  # or inspect.ismethod(value):
                    # TODO: Turn parameter-less function into switch
                    if (
                        module.__name__ == value.__module__
                        and not name.startswith(', '.join(excludes))
                    ):
                        if command:
                            # apply command name scheme
                            if self.command_scheme == 'chain':
                                cmd_name = module_name + '.' + name
                            else:
                                cmd_name = name
                            msg = parse(value.__doc__).short_description
                            cmd = command.add_parser(
                                cmd_name.replace('_', '-'),
                                description=msg,
                                formatter_class=ArgufyHelpFormatter,
                                help=msg,
                            )
                            cmd.set_defaults(fn=value)
                            parser.formatter_class = ArgufyHelpFormatter
                        # log.debug(f"command {name} {value} {cmd}")
                        self.add_arguments(value, cmd)

                # create arguments from module varibles
                elif isinstance(value, (float, int, str, list, dict, tuple)):
                    # TODO: Reconcile inspect parameters with dict
                    parameters = inspect.Parameter(
                        name,
                        _ParameterKind.POSITIONAL_OR_KEYWORD,  # type: ignore
                        default=getattr(module, name),
                        annotation=inspect._empty,  # type: ignore
                    )
                    description = next(
                        (d for d in docstring.params if d.arg_name == name),
                        None,
                    )
                    arguments = self.__get_args(
                        Argument(parameters, description)
                    )
                    name = arguments.pop('name')
                    parser.add_argument(*name, **arguments)
        return self

    def __set_module_arguments(
        self, fn: Callable[[F], F], ns: Namespace
    ) -> Namespace:
        '''Separe module arguments from functions.'''
        if 'mod' in ns:
            mod = vars(ns).pop('mod')
        else:
            mod = None

        # separate namespace from other variables
        signature = inspect.signature(fn)
        args = [
            {k: vars(ns).pop(k)}
            for k in list(vars(ns).keys()).copy()
            if not signature.parameters.get(k)
        ]

        # set module variables
        if mod:
            for arg in args:
                for k, v in arg.items():
                    mod.__dict__[k] = v
        return ns

    def retrieve(
        self,
        args: Sequence[str] = sys.argv[1:],
        ns: Optional[Namespace] = None,
    ) -> Tuple[List[str], Namespace]:
        '''Retrieve values from CLI.'''
        # TODO: handle invalid argument

        # show help when no arguments provided
        if args == []:
            args = ['--help']  # pragma: no cover
        main_ns, main_args = self.parse_known_args(args, ns)
        if main_args == [] and 'fn' in vars(main_ns):
            return main_args, main_ns
        else:
            # default to help message for subcommand
            if 'mod' in vars(main_ns):
                a = []
                a.append(vars(main_ns)['mod'].__name__.split('.')[-1])
                a.append('--help')
                self.parse_args(a)
            return main_args, main_ns

    def dispatch(
        self,
        args: Sequence[str] = sys.argv[1:],
        ns: Optional[Namespace] = None,
    ) -> Optional[Callable[[F], F]]:
        '''Call command with arguments.'''
        # TODO: support command chaining at same level

        # parse variables
        arguments, namespace = self.retrieve(args, ns)
        # log.debug("%s %s", arguments, namespace)

        # call function with variables
        if 'fn' in namespace:
            fn = vars(namespace).pop('fn')
            namespace = self.__set_module_arguments(fn, namespace)
            fn(**vars(namespace))
        return self.dispatch(arguments) if arguments != [] else None
