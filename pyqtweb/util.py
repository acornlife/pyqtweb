import inspect


def list_bind_funcs(obj):
    return {
        name: inspect.getfullargspec(getattr(obj, name)).args[1:] for name in dir(obj) if
        not name.startswith('_') and inspect.ismethod(getattr(obj, name))
    }
