#!/opt/local/bin/python
# Copyright 2014, Octoboxy LLC.  All Rights Reserved.
''' Functions for modules, callstacks, thread names, etc. '''

import inspect
import socket
import subprocess
import threading


def ImportCapitalizedNamesFrom(*modulelist):
  ''' Like doing `from module import *` but pulls in only names that start with capitals. '''
  globs             = GetGlobalsOfCaller()
  for module in modulelist:
    for key in module.__dir__():
      if key[0] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' and not key in globs:
        globs[key]  = getattr(module, key)


def GetGlobalsOfCaller():
  ''' Retrieves the globals() of the module that called the code that called this function. '''
  try:
    frame         = None
    stack         = inspect.stack()
    if len(stack) >= 3:
      frame       = stack[2][0]
    elif len(stack) == 2:
      frame       = stack[1][0]
    return frame and frame.f_globals
  finally:
    del frame


def IsA(item, parent):
  ''' Returns True if item is an instance or subclass of parent. '''
  if item == parent:
    return True
  if not item or not parent:
    return False
  if not isinstance(parent, type):
    parent      = type(parent)
  if isinstance(item, parent):
    return True
  if isinstance(item, type):
    return issubclass(item, parent)


def ParentTypes(thing):
  ''' Returns a list of the types that a thing derives from. '''
  if not isinstance(thing, type):
    thing         = type(thing)
  supermros       = set()
  for parent in thing.__mro__[1:]:
    for notours in parent.__mro__[1:]:
      supermros.add(notours)
  return [x for x in thing.__mro__[1:] if x != object and x not in supermros]


def ClassName(o):
  ''' Returns a string for the python class name of object o. '''
  # If the object came from a query with deferred fields, we need the parent model, not the proxy
  # with a name like 'File_Deferred_bytes_extension_hash_parent_hash_s07da85ef0c792d44433336a3d733f56c'
  if hasattr(o, '_meta'):
    if hasattr(o._meta, 'proxy_for_model'):
      if o._meta.proxy_for_model:
        o = o._meta.proxy_for_model

  # The rest is simple
  try:
    return o.__name__
  except AttributeError:
    return type(o).__name__


def AppName(o):
  ''' Returns a string for the Django app a class is defined in. '''
  if hasattr(o, '__module__') and isinstance(o.__module__, type('')):
    return o.__module__.split('.')[0]
  if hasattr(o, '__class__') and hasattr(o.__class__, '__module__') and isinstance(o.__class__.__module__, type('')):
    return o.__class__.__module__.split('.')[0]
  return None


def ObjectName(o):
  ''' Convenience wrapper for the two above functions. '''
  return '{}.{}'.format(AppName(o), ClassName(o))


def ThreadName():
  ''' Returns the name of our current thread. '''
  return threading.current_thread().name


def HostName():
  ''' Returns the normalized hostname for the machine we're running on.
      UNLESS: we can detect we're on OS X, at which point we return the computer name
      that's been set in sharing system settings, regardless of whether DHCP has
      given our machine a new hostname or not.
  '''
  global _hostname_cache
  if not _hostname_cache:
    try:
      name        = subprocess.check_output(['scutil', '--get', 'ComputerName'], universal_newlines=True)
      name        = name and name.strip() or None
    except Exception:
      name        = None
    if not name:
      name        = socket.gethostname()
    name          = name and '.' in name and name.split('.', 1)[0] or name
    name          = name and name.lower() or None
    _hostname_cache = name
  return _hostname_cache
_hostname_cache   = None
