# -*- coding: utf-8 -*-
# Intro: 目录引入模块
# Author: Ztj
# Email: ztj1993@gmail.com
# Version: 0.0.3
# Date: 2020-01-03

import importlib
import pkgutil

__version__ = '0.0.3'


class DirImport(object):
    """目录引入模块"""

    def __init__(self, prefix, directory=None):
        self.modules = dict()
        self.prefix = prefix
        self.directory = list()

        if directory is not None:
            self.dir(directory)
            self.load()

    def dir(self, directory):
        """添加目录"""
        self.directory.append(directory)

    def load(self):
        """加载模块"""
        path = self.directory
        prefix = self.prefix + '.'
        for _, file, _ in pkgutil.iter_modules(path, prefix):
            self.modules[file] = importlib.import_module(file)

    def exclude(self, alias):
        """排除模块"""
        alias = [alias] if isinstance(alias, str) else alias
        for name in alias:
            self.modules.pop(name)

    def filter(self, var=None):
        """过滤模块"""
        exclude = []
        for name, module in self.modules.items():
            if not hasattr(module, var):
                exclude.append(name)
        self.exclude(exclude)

    def enable(self, var='enable'):
        """启用模块"""
        exclude = []
        for name, module in self.modules.items():
            if not hasattr(module, var):
                exclude.append(name)
            elif not getattr(module, var):
                exclude.append(name)
        self.exclude(exclude)

    def disable(self, var='disable'):
        """禁用模块"""
        exclude = []
        for name, module in self.modules.items():
            if hasattr(module, var) and getattr(module, var):
                exclude.append(name)
        self.exclude(exclude)

    def allow(self, alias):
        """允许模块"""
        exclude = []
        alias = [alias] if isinstance(alias, str) else alias
        for name in alias:
            if name not in self.modules:
                exclude.append(name)
        self.exclude(exclude)

    def get(self, name):
        return self.modules.get(name)

    def all(self):
        return self.modules

    def group(self, var):
        modules = dict()
        for name, module in self.modules.items():
            if not hasattr(module, var):
                continue
            if not isinstance(modules.get(getattr(module, var)), dict):
                modules[getattr(module, var)] = dict()
            modules[getattr(module, var)][name] = module
        return modules

    def call(self, var, *args, **kwargs):
        modules = dict()
        for name, module in self.modules.items():
            if not hasattr(module, var):
                continue
            modules[name] = getattr(module, var)(*args, **kwargs)
        return modules
