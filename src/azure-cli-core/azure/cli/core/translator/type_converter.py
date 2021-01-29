import inspect
import types


class AzTypeConverter:

    def __call__(self, value):
        raise NotImplementedError()

    def __str__(self):
        raise NotImplementedError()


class AzFuncTypeConverter(AzTypeConverter):

    def __init__(self, func):
        if not isinstance(func, types.FunctionType):
            raise TypeError('Expect a function. Got {}'.format(type(func)))
        self.import_module = inspect.getmodule(func).__name__
        self.import_name = func.__name__
        self.func = func

    def __call__(self, value):
        return self.func(value)

    def __str__(self):
        return "{}#{}".format(self.import_module, self.import_name)


class AzFuncTypeConverterByFactory(AzTypeConverter):

    def __init__(self, factory, args, kwargs):
        if isinstance(factory, types.FunctionType):     # support a factory function which return value is callable
            sig = inspect.signature(factory)
        elif isinstance(factory, type):
            # SizeWithUnitConverter
            sig = inspect.signature(factory.__init__)
        else:
            raise TypeError("Expect a function or a class. Got {}".format(type(factory)))

        self.import_module = inspect.getmodule(factory).__name__
        self.import_name = factory.__name__
        self.kwargs = {}
        if len(args) > 0:
            keys = list(sig.parameters.keys())
            if keys[0] == 'self':
                keys = keys[1:]
            keys = keys[:len(args)]
            for key, value in zip(keys, args):
                self.kwargs[key] = value
        self.kwargs.update(kwargs)
        self.instance = factory(*args, **kwargs)
        if not callable(self.instance):
            raise TypeError('Expect a callable instance.')

    def __call__(self, value):
        return self.instance(value)

    def __str__(self):
        return "{}#{}".format(self.import_module, self.import_name)


class AzLocationNameTypeConverter(AzTypeConverter):

    def __init__(self, cli_ctx):
        self.cli_ctx = cli_ctx
        self.import_module = inspect.getmodule(self).__name__
        self.import_name = self.__class__.__name__
        self.kwargs = {
            'cli_ctx': 'cli_ctx'
        }

    def __call__(self, name):
        from azure.cli.core.commands.parameters import get_subscription_locations
        if ' ' in name:
            # if display name is provided, attempt to convert to short form name
            name = next((location.name for location in get_subscription_locations(self.cli_ctx)
                         if location.display_name.lower() == name.lower()), name)
        return name

    def __str__(self):
        return "{}#{}".format(self.import_module, self.import_name)


def func_type_converter_wrapper(func):
    return AzFuncTypeConverter(func)

