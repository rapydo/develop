# -*- coding: utf-8 -*-

from invoke import Collection, Program, Config  # , Argument
from develop import __version__
from develop import coms as tasks


class DoConfig(Config):
    prefix = 'cmd'
    # env_prefix = 'TEST'


class MyProgram(Program):
    def core_args(self):
        core_args = super(MyProgram, self).core_args()
        extra_args = [
            # Argument(
            #     name='services',
            #     help="This was added by Paulie"
            # ),
        ]
        return core_args + extra_args


program = MyProgram(
    namespace=Collection.from_module(tasks),
    version=__version__
)
