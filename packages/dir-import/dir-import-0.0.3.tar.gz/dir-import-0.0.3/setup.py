# -*- coding: utf-8 -*-
# Intro: 目录模块加载
# Author: Ztj
# Email: ztj1993@gmail.com

import os.path
import re

from setuptools import setup

f = open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf8')
readme = f.read()
f.close()

f = open(os.path.join(os.path.dirname(__file__), 'ZtjDirImport.py'), encoding='utf8')
version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)
f.close()

setup(
    name='dir-import',
    version=version,
    description='python directory module import package',
    long_description=readme,
    long_description_content_type='text/markdown',
    py_modules=['ZtjDirImport'],
    url='https://github.com/ztj1993/py-dir-import',
    author='ZhangTianJie',
    author_email='ztj1993@gmail.com',
    keywords='directory module import',
    license='MIT License',
)
