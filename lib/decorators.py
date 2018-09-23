import argparse
import sys
import json

from .utils import as_obj, add_method, POJO

def command_arg(*args, **kwargs):
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
    def __init__(self, name, help, args):
        self.delegate = None
        self.help = help
        self.name = name
        self.args = args

    def add_delegate(self, delegate):
        self.delegate = delegate

    def has_arguments(self):
        return len(self.args) > 0

    def add_arguments(self, parser):
        for arg in self.args:
            parser.add_argument(*arg.args, **arg.kwargs)

    def process_kwargs(self, args):
        kwargs = {}
        for arg in self.args:
            argname = arg.get_name()
            if getattr(args, argname, False):
                kwargs[argname] = getattr(args, argname)
        return kwargs

def command(name='', help=None, args=list()):
    command = Command(name=name, help=help, args=args)
    def decorated(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        command.add_delegate(wrapper)
        setattr(wrapper, 'command', command)
        return wrapper
    return decorated

def with_commands(description):
    def wrapped(Cls):
        class CommandedCls:
            def __init__(self, *args, **kwargs):
                self.instance = Cls(*args, **kwargs)
                self.description = description
                self.bindings = self.list_bindings()
                self.parser = argparse.ArgumentParser(description=description)

            def run(self):
                self.add_commands()
                self.parse_args()

            def __getattribute__(self, attr):
                _attr = None
                try:
                    _attr = super(CommandedCls, self).__getattribute__(attr)
                except:
                    pass
                if _attr is None:
                    _attr = self.instance.__getattribute__(self.instance, attr)
                return _attr

            def add_commands(self):
                bindings = self.bindings.items()
                subparsers = self.parser.add_subparsers()
                for key, binding in bindings:
                    command_parser = subparsers.add_parser(key,
                        help=binding.command.help)
                    command_parser.set_defaults(command=key)

                    if binding.command.has_arguments():
                        binding.command.add_arguments(command_parser)

            def parse_args(self):
                args = self.parser.parse_args()
                if args.command:
                    binding = self.bindings.get(args.command)
                    command = binding.command
                    method = binding.method
                    kwargs = command.process_kwargs(args)
                    json_result = getattr(self.instance, args.command)(**kwargs)
                    print(
                        json.dumps(json_result, indent=4)
                        # method(self.instance, **kwargs)
                    )
                else:
                    self.parser.print_help()

            def is_valid_name(self, name):
                return not name.startswith('__')

            def is_decorated(self, name):
                method = getattr(self.instance, name)
                command = getattr(method, 'command', None)
                return command is not None


            def list_bindings(self):
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
                    name: as_obj({
                        "command": command,
                        "method": method
                    }) for [
                        name,
                        method,
                        command
                    ] in map(_getcommand, all_command_names)
                }
        return CommandedCls
    return wrapped
