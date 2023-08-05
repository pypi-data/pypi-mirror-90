import importlib
import inspect
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar

import uvicore

from uvicore.contracts import Ioc as IocInterface
from uvicore.support import module
from uvicore.support.dumper import dd, dump
from uvicore.container import Binding

T = TypeVar('T')


class _Ioc(IocInterface):
    """Inversion of Control private class.

    Do not import from this location.
    Use the uvicore.ioc singleton global instead."""

    @property
    def bindings(self) -> Dict[str, Binding]:
        return self._bindings

    @property
    def overrides(self) -> Dict[str, str]:
        # Merge app config bindings with registered overrides (app config wins)
        app_config_overrides = self._app_config.get('bindings') or {}
        overrides = {**self._overrides, **app_config_overrides}
        return overrides

    @property
    def aliases(self) -> Dict[str, str]:
        return self._aliases

    def __init__(self, app_config: Dict) -> None:
        self._bindings: Dict[str, Binding] = {}
        self._aliases: Dict[str, str] = {}
        self._app_config = app_config
        self._overrides: Dict[str, str] = {}


        # Add default binding specific to uvicore framework
        # Only some early defaults are here.  The rest are bound in
        # their service providers register() method
        # NO - Deprecated now that I can bind default and make
        self.bind_map({
            #'Application': {
            #    'object': 'uvicore.foundation.application._Application',
            #    'singleton': True,
            #    'aliases': ['App', 'app', 'application'],
            #},
            #'ServiceProvider': {
            #    'object': 'uvicore.package.provider._ServiceProvider',
            #    'aliases': ['service', 'provider'],
            #},
            #'Package': {
            #    'object': 'uvicore.package.package._Package',
            #    'aliases': ['package'],
            #},
            #'Dispatcher': {
            #    'object': 'uvicore.events.dispatcher._Dispatcher',
            #    'singleton': True,
            #    'aliases': ['dispatcher', 'Event', 'event', 'Events', 'events'],
            #},
        })

    #def config(self, config: Dict) -> None:
    #    self._app_config = config

    def binding(self, name: str) -> Binding:
        if name in self.bindings:
            return self.bindings[name]
        elif name in self.aliases:
            return self.bindings[self.aliases[name]]

    def make(self, name: str, default: Callable[[], T] = None, **kwargs) -> T:
        if default is not None and self.binding(name) is None:
            # Default was provided and no binding currently exists
            # Bind the default provided but look for bindings override in app_config
            #object = default
            #bindings = self._app_config.get('bindings') or {}
            #object = bindings.get(name) or default
            object = self.overrides.get(name) or default
            self.bind(name, object, **kwargs)

        binding = self.binding(name)
        if not binding:
            # No binding set yet.  If we simply try to import the file only, it may have a
            # decorator that will bind itself.  If no binding found even after import, treat as not found
            if '.' in name: module.load(name)

            # Check binding again
            binding = self.binding(name)
            if not binding:
                raise ModuleNotFoundError("Could not find IoC name '{}' in mapping.".format(name))

        # If object is not defined, dynamically import it on first make (deferred)
        if not binding.object:
            # If object is None, dynamically import object from path
            binding.object = module.load(binding.path).object

        # Determine type
        is_class = inspect.isclass(binding.object)
        is_singleton = is_class and binding.singleton
        kwargs = binding.kwargs or {}

        # Odd case
        if not is_class and binding.singleton and hasattr(binding.object, '__class__') and '.' in str(getattr(binding.object, '__class__')):
            # If you override a singlton with another singleton (in the case of overriding a table for example)
            # You get an odd case where the binding object is the singleton itself.  So here we detect if the object
            # should be a singleton, and is NOT a class (because its already a singleton instance) and the object
            # is an instance (meaning it has a __class__ attribute) then we need to swap the instance with the object
            # and set the objects name to the instances __class__
            # By checking if __class__ has a . in it we skip over if someone accidentally added a singleton to a function or method
            # In case you are wondering, the singleton of the original IS the same singleton as the override!
            binding.instance = binding.object
            binding.object = binding.instance.__class__
            is_singleton = True

        # Instantiate a singleton only once
        made = None
        if is_singleton:
            if not binding.instance:
                if binding.factory:
                    factory = module.load(binding.factory).object
                    binding.instance = factory().make(binding.object, **kwargs)
                else:
                    binding.instance = binding.object(**kwargs)
            made = binding.instance

        # Instantiate a non-singleton every time
        # Unless there is no factory and no kwargs, simply return the object class
        elif is_class:
            if binding.factory:
                if type(binding.factory) == str:
                    # String factory, dynamically import it
                    factory = module.load(binding.factory).object
                else:
                    # Direct class factory
                    factory = binding.factory
                made = factory().make(binding.object, **kwargs)
            elif binding.kwargs:
                made = binding.object(**kwargs)
            else:
                made = binding.object

        # Bind is not a class.  Must be a method or module, return it
        else:
            made = binding.object

        # Return made object
        return made

    def bind_from_decorator(self, cls, name: str = None, *, object_type: str = None, factory: Any = None, kwargs: Dict = None, singleton: bool = False, aliases: List = []) -> None:
        #overrides = self._app_config.get('bindings') or {}

        # Merge app config bindings with registered overrides (app config wins)
        #overrides = {**self.overrides, **overrides}

        # Check for an override binding in the running app_config
        #override = overrides.get(name)
        override = self.overrides.get(name)

        # We never override an existing binding from a decorator
        #if name not in self.bindings:
        if override:
            self.bind(name=name, object=override, object_type=object_type, factory=factory, kwargs=kwargs, singleton=singleton, aliases=aliases)

            # Also bind the original so I can import it to override it.  Originals should never be a singleton
            # We solve circular dependencies by adding the cls right to the binding, so it never has to import it!
            self.bind(name + '_BASE', cls, object_type=object_type, factory=factory, kwargs=kwargs, singleton=False, aliases=aliases)
        else:
            # No override, so add binding to this cls object directly (not a string)
            self.bind(name, cls, object_type=object_type, factory=factory, kwargs=kwargs, singleton=singleton, aliases=aliases)


        # else:
        #     # Binding already exists and decorators never override existing bindings.  If existing binding is the same class as this decorator is on
        #     # add in the cls so .make() doesn't have to "import" the same class (causing circular import issues).  If its not the same class, .make() will
        #     # make and import it as usual.
        #     if self.bindings[name].path == name and self.bindings[name].object is None:
        #         self._bindings[name].object = cls
        #         self._bindings[name].type = object_type

        # Finally return the actual bind make, which if overridden, could be a completely different object!
        return self.make(name)

    def _bind_decorator(self, name: str = None, *, object_type: str = None, factory: Any = None, kwargs: Dict = None, singleton: bool = False, aliases: List = []) -> None:
        def decorator(cls):
            bind_name = name or cls.__module__ + '.' + cls.__name__
            # Decorator bindings are always override=False
            return self.bind_from_decorator(cls, name=bind_name, override=False, factory=factory, kwargs=kwargs, singleton=singleton, aliases=aliases)
        return decorator

    def bind_override(self, name: str, object: str):
        self._overrides[name] = object

    def bind(self, name: str = None, object: Any = None, *, object_type: str = 'service', override: bool = True, factory: Any = None, kwargs: Dict = None, singleton: bool = False, aliases: List = []) -> None:
        # Decorator Usage
        if object is None: return self._bind_decorator(name, object_type=object_type, factory=factory, kwargs=kwargs, singleton=singleton, aliases=aliases)

        # Add each aliases to list of all aliases
        for alias in aliases:
            self._aliases[alias] = name

        # Set path and object based on str or actual class
        path = None
        if type(object) == str:
            path = object
            object = None

        if path is None and object is not None:
            if hasattr(object, '__module__') and hasattr(object, '__name__'):
                path = object.__module__ + '.' + object.__name__
            else:
                path = name

        # Add binding, obeying override
        if override == True or name not in self.bindings:
            #print(name, '----', path)
            self._bindings[name] = Binding(
                path=path,
                object=object,
                instance=None,
                type=object_type,
                factory=factory,
                kwargs=kwargs,
                singleton=singleton,
                aliases=aliases,
            )

    def bind_map(self, mapping: Dict[str, Dict]) -> None:
        # bind_map is not used anymore, though could be cool if passed through from provider class as well, if ever
        for name, options in mapping.items():
            self.bind(name, **options)

    def alias(self, src: str, dest: str) -> None:
        if dest not in self.bindings:
            raise Exception('Could not find IoC binding '.format(dest))
        if src not in self.bindings[dest]:
            self.bindings[dest].aliases.append(src)
