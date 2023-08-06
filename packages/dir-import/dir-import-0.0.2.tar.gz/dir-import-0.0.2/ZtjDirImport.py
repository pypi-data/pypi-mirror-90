# -*- coding: utf-8 -*-
# Intro: 目录模块加载
# Author: Ztj
# Email: ztj1993@gmail.com
# Version: 0.0.2
# Date: 2020-01-03

import importlib
import pkgutil

__version__ = '0.0.2'


class DirImport(object):
    """目录模块加载"""

    def __init__(self, path=None):
        self.mods = dict()
        self.load(path)

    def load(self, path):
        mod = importlib.import_module(path)
        for _, file, _ in pkgutil.iter_modules(path=mod.__path__, prefix=mod.__name__ + '.'):
            self.mods[file] = importlib.import_module(file)

    def get(self, name):
        return self.mods.get(name)

    def all(self):
        return self.mods

    def group(self, var):
        mods = dict()
        for name, mod in self.mods.items():
            if not hasattr(mod, var):
                continue
            if not isinstance(mods.get(getattr(mod, var)), dict):
                mods[getattr(mod, var)] = dict()
            mods[getattr(mod, var)][name] = mod
        return mods

    def filter(self, var):
        exclude = []
        for name, mod in self.mods.items():
            if not hasattr(mod, var):
                exclude.append(name)
            if getattr(mod, var) is False:
                exclude.append(name)
        for name in exclude:
            self.mods.pop(name)
        return self

    def call(self, var, *args, **kwargs):
        mods = dict()
        for name, mod in self.mods.items():
            if not hasattr(mod, var):
                continue
            mods[name] = getattr(mod, var)(*args, **kwargs)
        return mods
