#!/usr/bin/python -tt

""" 
Simplistic Python SysFS interface.

Shamelessly stolen from:
    http://stackoverflow.com/questions/4648792/

Usage::
    from sysfs import sys

    for bdev in sys.block:
        print bdev, str(int(bdev.size) / 1024 / 1024) + 'M'
"""

__all__ = ['sys', 'Node']

from os import listdir
import stat
import types
from os.path import join

def isfile(self, f):
    return stat.S_ISREG(self.stat(f).st_mode)

def isdir(self, f):
    return stat.S_ISDIR(self.stat(f).st_mode)

def _mp(obj):
    obj.isfile = types.MethodType(isfile, obj)
    obj.isdir = types.MethodType(isdir, obj)


class Node(object):
    __slots__ = ['_path_', '_conn_', '__dict__']

    def __init__(self, sftp, path='/sys'):
        self._conn_ = sftp
        _mp(sftp)
        self._path_ = self._conn_.normalize(path)
        if not self._path_.startswith('/sys/') and not '/sys' == self._path_:
            raise RuntimeError('Using this on non-sysfs files is dangerous!')

        self.__dict__.update(dict.fromkeys(self._conn_.listdir(self._path_)))

    def __repr__(self):
        return '<rsysfs.Node "%s" via "%s" >' % self._path_, self._

    def __str__(self):
        return (self._path_)

    def __setattr__(self, name, val):
        if name.startswith('_'):
            if name == "_conn_":
                _mp(val)
            return object.__setattr__(self, name, val)

        path = self._conn_.normalize(join(self._path_, name))
        if self._conn_.isfile(path):
            with self._conn_.file(path, 'w') as fp:
                fp.write(val)
        else:
            raise RuntimeError('Cannot write to non-files.')

    def __getattribute__(self, name):
        if name.startswith('_'):
            return object.__getattribute__(self, name)

        path = self._conn_.normalize(join(self._path_, name))
        if self._conn_.isfile(path):
            with self._conn_.file(path, 'r') as fp:
                return fp.read().strip()
        elif self._conn_.isdir(path):
            return Node(self._conn_, path)

    def __setitem__(self, name, val):
        return setattr(self, name, val)

    def __getitem__(self, name):
        return getattr(self, name)

    def __iter__(self):
        return iter(getattr(self, name) for name in listdir(self._path_))

sys = None

# vim:set sw=4 ts=4 et:
# -*- coding: utf-8 -*-
