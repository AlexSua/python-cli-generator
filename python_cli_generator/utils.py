import functools
import importlib
import types

from inspect import Parameter, signature
from typing import List


def include_custom_signature_parameters(fn, custom_signature_parameters: List[Parameter] = None):
    if custom_signature_parameters is None:
        return fn
    else:
        sig = signature(fn)
        parameters = tuple(sig.parameters.values())
        variadic = 0
        for parameter in parameters:
            if not parameter.kind == 4:
                variadic += 1
        parameters = parameters[0:variadic] + \
            tuple(custom_signature_parameters) + parameters[variadic:]
        sig = sig.replace(parameters=parameters)
        fn.__signature__ = sig
        return fn


def decorator_factory(call, custom_signature_parameters: List[Parameter] = None, **kwargs):

    def _decorator(fn):

        fn = include_custom_signature_parameters(
            fn, custom_signature_parameters)

        @functools.wraps(fn)
        def _wrapped(
            *args,
            **kwargs,
        ):
            return call(fn, *args, **kwargs)

        return _wrapped

    return _decorator


class LazyImport(types.ModuleType):
    def __init__(self, name, className):
        super(LazyImport, self).__init__(name)
        self.module = None
        self.name = name
        self.className = className

    def __call__(self, *args, **kwds):
        if self.module is None:
            self.module = importlib.import_module(self.name)
        return self.module.__dict__[self.className](*args, **kwds)