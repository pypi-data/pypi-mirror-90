# --------------------------------------------------------------------
# attributes.py
#
# Author: Lain Musgrove (lain.proliant@gmail.com)
# Date: Thursday May 7, 2020
#
# Distributed under terms of the MIT license.
# --------------------------------------------------------------------

import inspect
from typing import List
from .utils import get_params_from_signature, bind_unbound_method
from .errors import InjectionError


# --------------------------------------------------------------------
NOTHING = object()


# --------------------------------------------------------------------
class Attributes:
    def __init__(self):
        self.attr_map = {}

    @staticmethod
    def for_object(obj, create=True, write=False,
                   factory=lambda: Attributes()):
        try:
            return obj._attrs

        except AttributeError:
            if create:
                attrs = factory(obj)
                if write:
                    obj._attrs = attrs
                return attrs
            return None

    def put(self, attr, value=True):
        self.attr_map[attr] = value
        return self

    def get(self, attr, default_value=NOTHING):
        if attr in self.attr_map:
            return self.attr_map[attr]
        if default_value is NOTHING:
            raise AttributeError("No such attribute: %s" % attr)
        return default_value

    def check(self, attr):
        return bool(self.get(attr, None))

    def has(self, attr):
        return self.get(attr, None) is not None

    def merge(self, attr):
        self.attr_map.update(attr.attr_map)
        return self


# --------------------------------------------------------------------
class ClassAttributes(Attributes):
    @staticmethod
    def for_class(class_, create=True, write=False):
        return Attributes.for_object(
            class_, create, write, factory=lambda x: ClassAttributes(x)
        )

    @staticmethod
    def for_object(obj, create=True, write=False):
        return ClassAttributes.for_class(obj.__class__, create, write)

    def __init__(self, class_):
        super().__init__()
        self.put("name", class_.__name__)
        self.put("qualname", class_.__qualname__)
        self.put("doc", class_.__doc__)


# --------------------------------------------------------------------
class MethodAttributes(Attributes):
    @staticmethod
    def for_method(f, create=True, write=False):
        return Attributes.for_object(
            f, create, write, factory=lambda x: MethodAttributes(x)
        )

    @staticmethod
    def wraps(f1):
        def decorator(f2):
            attr1 = MethodAttributes.for_method(f1)
            MethodAttributes.for_method(f2, write=True).merge(attr1)
            return f2

        return decorator

    @staticmethod
    def add(name, value=True):
        def decorator(f):
            attrs = MethodAttributes.for_method(f, write=True)
            attrs.put(name, value)
            return f

        return decorator

    def __init__(self, f):
        super().__init__()
        self.put("name", f.__name__)
        self.put("qualname", f.__qualname__)
        self.put("params", get_params_from_signature(f))
        self.put("doc", f.__doc__)


# --------------------------------------------------------------------
def get_injection_params(f, unbound_ctor=False):
    """
    Fetches the injectable parameter names of parameters to the given
    method, along with a set of parameters which have default values
    and should be considered optional dependencies.

    This method will throw InjectionError if the method provided has
    arguments that are not POSITIONAL_OR_KEYWORD or KEYWORD_ONLY.

    If the method provided is an unbound object constructor,
    unbound_ctor must be set to True to prevent 'self' from being
    returned by this method as an injectable parameter.
    """
    injection_param_names = []
    default_param_set = set()
    params: List = []

    if not inspect.ismethod(f) and unbound_ctor and not inspect.isfunction(f):
        # We do not want to try to inject a slot wrapper
        # version of __init__, as its params are (*args, **kwargs)
        # and it does nothing anyway.
        return [], set()

    attr = MethodAttributes.for_method(f)
    if attr.has("params"):
        params = attr.get("params")
    else:
        params = get_params_from_signature(f)

    if inspect.ismethod(f) or unbound_ctor:
        # Don't try to inject the 'self' parameter of an
        # unbound constructor.
        params = params[1:]

    for param in params:
        if param.kind in [
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                inspect.Parameter.KEYWORD_ONLY]:
            if param.default != param.empty:
                default_param_set.add(param.name)
            injection_param_names.append(param.name)
        else:
            raise InjectionError(
                "Xeno only supports injection of POSITIONAL_OR_KEYWORD and "
                "KEYWORD_ONLY arguments, %s arguments (%s of %s) "
                "are not supported."
                % (param.kind, param.name, f.__qualname__)
            )
    return injection_param_names, default_param_set


# --------------------------------------------------------------------
def scan_methods(obj, filter_f):
    """
    Scan the object for methods that match the given attribute filter
    and return them as a stream of tuples.
    """
    for class_ in inspect.getmro(obj.__class__):
        for name, method in inspect.getmembers(class_,
                                               predicate=inspect.isfunction):
            attrs = MethodAttributes.for_method(method, create=False)
            if attrs is not None and filter_f(attrs):
                yield (attrs, bind_unbound_method(obj, method))


# --------------------------------------------------------------------
def get_injection_points(obj):
    """
    Scan the object and all of its parents for injection points
    and return them as a stream of tuples.
    """

    return scan_methods(obj, lambda attr: attr.check("injection-point"))


# --------------------------------------------------------------------
def get_providers(obj):
    """
    Scan the object and all of its parents for providers and return
    them as a stream of tuples.
    """

    return scan_methods(obj, lambda attr: attr.check("provider"))
