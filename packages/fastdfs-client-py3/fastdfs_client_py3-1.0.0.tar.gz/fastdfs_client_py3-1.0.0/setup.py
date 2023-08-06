#!/usr/bin/env python
import os
from fdfs_client import __version__
try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension

f = open(os.path.join(os.path.dirname(__file__), 'README.md'))
long_description = f.read()
f.close()

sdict = {
    'name' : 'fastdfs_client_py3',
    'version' : __version__,
    'description' : 'Python3 and Python2 client for Fastdfs',
    'long_description' : long_description,
    'long_description_content_type': 'text/markdown',
    'author' : 'Huanglg',
    'author_email' : 'huanglg0425@gmail.com',
    'keywords':['Fastdfs', 'Distribute File System'],
    'license' : 'GPLV3',
    'packages' : ['fdfs_client']
    #'ext_modules' : [Extension('fdfs_client.sendfile',
    #                         sources = ['fdfs_client/sendfilemodule.c'])],
}


setup(**sdict)

