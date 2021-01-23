# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import inspect
import types


class AzValidator:

    def __call__(self, *args, **kwargs):
        raise NotImplementedError()

    def __str__(self):
        raise NotImplementedError()


class AzFuncValidator(AzValidator):

    def __init__(self, func):
        if not isinstance(func, types.FunctionType):
            raise TypeError('Expect a function. Got {}'.format(type(func)))
        self.module_name = inspect.getmodule(func).__name__
        self.name = func.__name__
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def __str__(self):
        return "{}#{}".format(self.module_name, self.name)


class AzPropertyFuncValidator(AzValidator):

    def __init__(self, func):
        pass


class AzClassValidator(AzValidator):

    def __init__(self, cls, args, kwargs):
        if isinstance(cls, types.FunctionType):     # support a function which return value is callable
            sig = inspect.signature(cls)
        elif isinstance(cls, type):
            sig = inspect.signature(cls.__init__)
        else:
            raise TypeError("Expect a function or a class. Got {}".format(type(cls)))

        self.module_name = inspect.getmodule(cls).__name__
        self.name = cls.__name__
        self.kwargs = {}
        if len(args) > 0:
            keys = list(sig.parameters.keys())
            if keys[0] == 'self':
                keys = keys[1:]
            keys = keys[:len(args)]
            for key, value in zip(keys, args):
                self.kwargs[key] = value
        self.kwargs.update(kwargs)
        self.instance = cls(*args, **kwargs)
        if not callable(self.instance):
            raise TypeError('Expect a callable instance.')

    def __call__(self, *args, **kwargs):
        self.instance(*args, **kwargs)

    def __str__(self):
        return "{}#{}".format(self.module_name, self.name)


def func_validator_wrapper(validator):
    return AzFuncValidator(validator)


def cls_validator_wrapper(validator_cls):
    def wrapper(*args, **kwargs):
        return AzClassValidator(validator_cls, args, kwargs)
    return wrapper
