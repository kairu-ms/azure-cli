# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import inspect
import types
from knack.arguments import CLIArgumentType


class AzArgType(CLIArgumentType):

    def __init__(self, instance):
        self._is_registed = False
        super(AzArgType, self).__init__(**instance.settings)
        self._is_registed = True

    def update(self, *args, **kwargs):
        if self._is_registed:
            raise NotImplementedError("Not support to update registered arg type")
        super(AzArgType, self).update(*args, **kwargs)


class AzArgTypeInstance(AzArgType):

    def __init__(self, instance, import_module, register_name):
        self.import_module = import_module
        self.register_name = register_name
        if not isinstance(instance, CLIArgumentType):
            raise TypeError('Expect type is CLIArgumentType. Got "{}"'.format(type(instance)))
        super(AzArgTypeInstance, self).__init__(instance=instance)


class AzArgTypeByFactory(AzArgType):

    def __init__(self, instance, factory, args, kwargs):
        if isinstance(factory, types.FunctionType):  # support a factory function which return value is callable
            sig = inspect.signature(factory)
        elif isinstance(factory, type):
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
        if not isinstance(instance, CLIArgumentType):
            raise TypeError('Expect type is CLIArgumentType. Got "{}"'.format(type(instance)))
        super(AzArgTypeByFactory, self).__init__(instance=instance)


def register_arg_type(instance, register_name):
    parent_frame = inspect.stack()[1].frame
    import_module = inspect.getmodule(parent_frame).__name__
    return AzArgTypeInstance(instance, import_module, register_name)


def arg_type_factory_wrapper(factory):
    def wrapper(*args, **kwargs):
        instance = factory(*args, **kwargs)
        if instance is None:
            return None
        else:
            return AzArgTypeByFactory(instance, factory, args, kwargs)
    return wrapper
