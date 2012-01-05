# coding=utf-8

"""Decorators used for wrapping attribute mapper functions.

For the time being, these will not be used in favor of __getattr__()
and __setattr__(). There's just way too much overhead to justify it.

@see http://adam.gomaa.us/blog/2008/aug/11/the-python-property-builtin/
"""

__author__ = "Patrick Jacobs <ceolwulf@gmail.com>"

import inspect

def auto_property(func):
    """Automagically return a property instance from method functions.

    Methods wishing to utilize this decorator should return a locals()
    call that itself returns getter, setter, and deleter functions. For
    example:
        
        class MyClass(object):
            ...
            @auto_property
            def my_attribute():
                def fget(self):
                    ...
                def fset(self, value):
                    ...
                return locals()
    """
    return property(**func())

def attr_property(func):
    """Wrap a get/set function as a property."""
    
    def fget(self):
        return func(self)
    
    def fset(self, value):
        return func(self, value)

    return property(fget, fset)

def decorate_class(decorator):
    """Wrap every method of a class in a decorator.

    @see http://stackoverflow.com/a/2238076/374470
    """

    def dec_cls(cls):
        for name, method in inspect.getmembers(cls, inspect.ismethod):
            if name != '__init__':
                setattr(cls, name, decorator(method))
        
        return cls
    
    return dec_cls