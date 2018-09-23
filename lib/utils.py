import sys

class POJO: pass
def as_obj(dc):
    obj = POJO()
    for key, val in dc.items(): setattr(obj, key, val)
    return obj

def read_stdin():
    return "\n".join(sys.stdin)

def add_method(obj, method, name=None):
    if name is None:
        name = method.__name__
    setattr(obj, name, method)

def with_commands(Cls):
    class CommandedCls:
        def __init__(self, *args, **kwargs):
            self.instance = Cls(*args, **kwargs)

        def __getattribute__(self, attr):
            return self.instance.__getattribute__(self, attr)

        def is_valid_name(self, name): return not name.startswith('__')
        def is_decorated(self, name):
            return getattr(
                getattr(self.instance, name),
                'decorated',
                None
            ) is not None

        def list_decorated_methods(self):
            return filter(
                self.is_decorated,
                filter(self.is_valid_name, dir(self.instance))
            )

        def list_commands(self):
            return list(
                map(
                    lambda name: getattr(self.instance, name).as_command(),
                    self.list_decorated_methods()
                )
            )
    return CommandedCls

def command(name=None, shortname=None, help=None, use_stdin=False):
    def as_command(decorated):
        return lambda: as_obj({
            "help": help,
            "shortname": shortname,
            "name": name,
            "use_stdin": use_stdin,
            "action": decorated
        })

    def decorated(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

    setattr(decorated, 'decorated', True)
    add_method(decorated, as_command(decorated))
    return decorated
