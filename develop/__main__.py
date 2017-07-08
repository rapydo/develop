# -*- coding: utf-8 -*-

from invoke import Collection, Program  # , Config, Argument
from develop import __version__
from develop.mytasks import package as package_operations


# class DoConfig(Config):
#     prefix = 'cmd'
#     # env_prefix = 'TEST'


class MyProgram(Program):

    # def core_args(self):
    #     core_args = super(MyProgram, self).core_args()
    #     extra_args = [
    #         # Argument(
    #         #     name='services',
    #         #     help="This was added by Paulie"
    #         # ),
    #     ]
    #     return core_args + extra_args

    def print_help(self):
        """
        Hacking the code base, src:
        https://github.com/pyinvoke/invoke/blob/master/invoke/program.py
        """

        # USAGE
        usage_suffix = "task1 [--task1-opts] ... taskN [--taskN-opts]"
        if self.namespace is not None:
            # usage_suffix = "<subcommand> [--subcommand-opts] ..."
            usage_suffix = "<command> [--command-opts] ..."
        # print(
        #     "Usage: {0} [--core-opts] {1}"
        #     .format(self.binary, usage_suffix))
        print("Usage: {0} {1}".format(self.binary, usage_suffix))
        print("")

        # OPTIONS TO BE OVERRIDDEN
        # print("Core options:")
        # print("")
        # self.print_columns(self.initial_context.help_tuples())

        if self.namespace is not None:
            self.list_tasks()


# Using namespaces for sub-sub commands
ns = Collection()
# ns.add_task()
ns.add_collection(package_operations)
program = MyProgram(namespace=ns, version=__version__)
