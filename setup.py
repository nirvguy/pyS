#!/usr/bin/env python3
from setuptools import setup
import pyS

from pyS import config

setup(name             = 'pyS',
      version          = config.VERSION,
      description      = 'A parser and interpreter for the Turing Complete S language (Davis/Sigal/Weyuker)',
      author           = 'Juan Cruz Sosa',
      author_email     = 'nirvguy@gmail.com',
      packages         = ['pyS'],
      install_requires = ['ply'],
      entry_points={
        'console_scripts': ['Scompiler = pyS.Scompiler:main',
                            'Sdump = pyS.Sdump:main'],
      }
)
