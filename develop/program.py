# -*- coding: utf-8 -*-

from invoke import Program, Argument


class CLIProgram(Program):
    """
    The invoke modified class for a command line program/application in Python
    # TODO: move into utilities to reduce dependencies
    """

    def __init__(self, version=None, namespace=None, extra_arguments=None):

        if extra_arguments is None:
            self.extra_args = []
        else:
            self.extra_args = extra_arguments

        self.extra_args.append(
            Argument(
                name='log-level',
                help="set the application log level"
            )
        )

        super(CLIProgram, self).__init__(version=version, namespace=namespace)

    @staticmethod
    def setup_logger():
        from utilities import apiclient
        level = apiclient.check_cli_arg('log-level', get=True)
        return apiclient.setup_logger(__name__, level_name=level)

    def core_args(self):
        core_args = super(CLIProgram, self).core_args()
        # for core in core_args:
        #     from beeprint import pp
        #     pp(core)
        return core_args + self.extra_args

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

        print("Core options:")
        print("")

        helps = [arg.help for arg in self.extra_args]
        tuples = []
        for mytuple in self.initial_context.help_tuples():
            if mytuple[1] in helps:
                tuples.append(mytuple)
        self.print_columns(tuples)

        if self.namespace is not None:
            self.list_tasks()
