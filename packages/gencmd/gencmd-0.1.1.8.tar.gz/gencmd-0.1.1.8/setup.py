#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, Extension
from Cython.Build import cythonize
import io
import os


package_version=open('.version', 'r').read()

def read(file_name):
    """Read a text file and return the content as a string."""
    with io.open(os.path.join(os.path.dirname(__file__), file_name),
                 encoding='utf-8') as f:
        return f.read()

setup(name='gencmd',
    description='Library for send commands to the video-core on Raspberry Pi',
    author='Vanya Usalko',
    author_email='ivict@rambler.ru',
    url="http://github.com/usalko/gencmd",
    version=package_version,
    py_modules=['gencmd'],
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    keywords="RPi vcore videocore cmd gencmd",
    license='Apache License 2.0',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    ext_modules = cythonize(
        [
            Extension('gencmd',
            sources=['c/gencmd.c', 'gencmd.v.c', 'gencmd.pyx'],
            library_dirs = ['/opt/vc/lib'],
            libraries=['vchiq_arm', 'bcm_host'],
            language='v',
            extra_compile_args=['-Ic', '-Ithirdparty/vc'],
            extra_link_args=[
                '-L./build/', '-Wl,-rpath,$ORIGIN',
                '-Wl,-rpath,/opt/vc/lib',
            ])
        ],
        compiler_directives={'language_level': '3'},
        gdb_debug=True
    )
)
