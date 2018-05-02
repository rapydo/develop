# -*- coding: utf-8 -*-

from setuptools import setup
from develop import \
    __version__ as current_version, \
    __package__ as main_package

app = '%s.__main__:program.run' % main_package

setup(
    name='rapydo-develop',
    version=current_version,
    description='Develop new features on RAPyDo framework',
    url='https://rapydo.github.io/develop',
    author="Paolo D'Onorio De Meo",
    author_email='p.donorio.de.meo@gmail.com',
    packages=[
        main_package
    ],
    install_requires=[
        'rapydo-utils==%s' % current_version,
        'invoke==0.23.0'
    ],
    entry_points={
        'console_scripts': [
            'develop = %s' % app,
            'dev = %s' % app,
        ]
    },
    classifiers=[
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords=['utilities', 'rapydo', 'logs', 'tools']
)
