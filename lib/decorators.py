import argparse
import sys
import json

from .utils import as_obj

def command_arg(*args, **kwargs):
    """
    Small tweak to build argparse.add_argument() arguments through a command
    declaration (see `command` decorator and `Command.add_arguments` method)
    """
    class CommandArg:
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

        def get_name(self):
            name = self.args[1] if len(self.args) > 1 else self.args[0]
            if name.startswith('--'):
                name = name[2:]
            return name

    return CommandArg(*args, **kwargs)


class Command(object):
    """
    The Command object represent a given action. In fine, its goal is to make
    the argparse.ArgumentParser parsing result in the calling of the method that
    used the @command decorator.
    """
    def __init__(self, name, help, args):
        self.help = help
        self.name = name
        self.args = args

    def has_arguments(self):
        return len(self.args) > 0

    def add_arguments(self, parser):
        for arg in self.args:
            parser.add_argument(*arg.args, **arg.kwargs)

    # Takes args produced by argparse.parse_args() and outputs the proper kwargs
    # dict for the bound api method.
    def process_kwargs(self, args):
        kwargs = {}
        for arg in self.args:
            argname = arg.get_name()
            if getattr(args, argname, False):
                kwargs[argname] = getattr(args, argname)
        return kwargs


def command(name='', help=None, args=list()):
    """
    @command() decorator. Used to register a sub command for argparse.
    To register arguments just use the command_arg() helper as you would with
    parser.add_argument() arguments.
    """
    command = Command(name=name, help=help, args=args)
    def decorated(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        setattr(wrapper, 'command', command)
        return wrapper
    return decorated

def with_commands(description):
    """
    Register a class as a commanded class. All methods marked with the @command()
    decorator will be be piloted from here.
    """
    def wrapped(Cls):
        class CommandedCls:
            def __init__(self, *args, **kwargs):
                self.instance = Cls(*args, **kwargs)
                self.description = description
                self.bindings = self.list_bindings()
                self.parser = argparse.ArgumentParser(description=description)

            def __getattribute__(self, attr):
                _attr = None
                try: _attr = super(CommandedCls, self).__getattribute__(attr)
                except: pass
                if _attr is None:
                    _attr = self.instance.__getattribute__(self.instance, attr)
                return _attr

            def run(self):
                self.add_commands()
                self.parse_args()

            def add_commands(self):
                bindings = self.bindings.items()
                subparsers = self.parser.add_subparsers()
                for key, binding in bindings:
                    command = binding.command
                    command_parser = subparsers.add_parser(key, help=command.help)
                    command_parser.set_defaults(command=key)
                    command.add_arguments(command_parser)

            def parse_args(self):
                args = self.parser.parse_args()
                if args.command:
                    binding = self.bindings.get(args.command)
                    command = binding.command
                    method = binding.method
                    kwargs = command.process_kwargs(args)
                    json_result = getattr(self.instance, args.command)(**kwargs)
                    print(json.dumps(json_result, indent=4))
                else:
                    self.parser.print_help()

            def is_valid_name(self, name): return not name.startswith('__')

            def is_decorated(self, name):
                """
                Check if a given command name is a decorated method
                """
                method = getattr(self.instance, name)
                return getattr(method, 'command', None) is not None

            def list_bindings(self):
                """
                Will return all decorated methods as a dict:
                {
                    <command name>: object(method=<bound api method>, command=<bound command object>),
                    ...
                }
                """
                all_command_names = filter(
                    self.is_decorated, filter(
                        self.is_valid_name,
                        dir(self.instance)
                    )
                )
                def _getcommand(name):
                    method = getattr(self.instance, name)
                    return [name, method, method.command]

                return {
                    name: as_obj({ "command": command, "method": method }) for [
                        name, method, command
                    ] in map(_getcommand, all_command_names)
                }

        return CommandedCls
    return wrapped
