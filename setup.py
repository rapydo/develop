# -*- coding: utf-8 -*-

from setuptools import setup
from develop import __version__, __package__ as main_package

app = '%s.__main__:program.run' % main_package

setup(
    name='rapydo-develop',
    version=__version__,
    packages=[
        main_package
    ],
    install_requires=[
        'rapydo-utils==0.5.0',
        'invoke==0.19.0',
    ],
    entry_points={
        'console_scripts': [
            'develop = %s' % app,
            'dev = %s' % app,
        ]
    }
)
