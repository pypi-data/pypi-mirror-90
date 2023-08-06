#!/opt/local/bin/python
# Copyright 2014, Octoboxy LLC.  All Rights Reserved.
''' The Registry allows simple name-based retrieval of Python objects. '''

import base
import logging
import threading


class Registry(metaclass=base.utils.Singleton):

  ###
  ## MetaClasses
  #

  class AutoRegisterClass(type):
    def __init__(klass, name, bases, dct):
      super().__init__(name, bases, dct)
      Registry().Register(klass)

  class AutoRegisterInstance(type):
    def __init__(klass, name, bases, dct):
      super().__init__(name, bases, dct)
      Registry().Register(klass())

  ###
  ## API
  #

  def Get(self, name, of_type=None):
    ''' Retrieve an object by name or return None. '''
    with self.lock:
      obj         = self.objects.get(name, None)
    if obj and of_type and not base.utils.IsA(obj, of_type):
      return None
    return obj

  def GetAll(self, of_type=None):
    ''' Retrieve all the objects we know of, or optionally only objects that descend from a certain type. '''
    with self.lock:
      if not of_type:
        return list(self.objects.values())
      if of_type in self.cache:
        return self.cache[of_type]
      results       = [o for o in self.objects.values()
          if o and isinstance(o, of_type)
          or (isinstance(o, type) and issubclass(o, of_type))]
      self.cache[of_type] = results
      return results

  def GetAllWithNames(self, of_type):
    ''' Retrieve (name, thing) for all the objects we know that descend from a certain type. '''
    with self.lock:
      results       = [(name, thing) for (name, thing) in self.objects.items()
          if thing and base.utils.IsA(thing, of_type)]
      return results

  def Register(self, obj, name=None):
    ''' An object would like to be part of the registry, please. '''
    if obj is None:
      raise base.errors.RegisteredObjectNotAllowedType()
    if not name:
      name          = base.utils.ObjectName(obj)
    with self.lock:
      if name in self.objects:
        raise base.errors.RegisteredObjectNameDuplication(name)
      self.objects[name]  = obj
      self.cache    = {}

  def UnRegister(self, name):
    ''' An object should be removed from the registry, please. '''
    if not type(name) == type(''):
      name          = base.utils.ObjectName(name)
    with self.lock:
      if not name in self.objects:
        raise base.errors.RegisteredObjectNotPresent(name)
      self.objects.pop(name)
      self.cache    = {}

  def UnRegisterByPrefix(self, prefix):
    ''' Remove all objects matching a name prefix, please. '''
    with self.lock:
      removes       = set()
      for name in self.objects:
        if name.startswith(prefix):
          removes.add(name)
      for name in removes:
        del self.objects[name]
      self.cache    = {}

  def __contains__(self, name):
    with self.lock:
      return name in self.objects

  ###
  ## Internals
  #

  def __init__(self):
    self.lock       = threading.RLock()
    self.objects    = {}    # { name: item }
    self.cache      = {}    # { type: registered items of that type }

  def __len__(self):
    with self.lock:
      return len(self.objects)

  def __bool__(self):
    with self.lock:
      return bool(self.objects)
