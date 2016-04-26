from __future__ import absolute_import, print_function, unicode_literals

from celery.bin.base import Command, Option
from celery.utils.imports import symbol_by_name


class cyanide(Command):

    def run(self, *names, **options):
        try:
            return self.run_suite(names, **options)
        except KeyboardInterrupt:
            print('interrupted by user: exiting...')

    def run_suite(self, names, suite, block_timeout=None, **options):
        return symbol_by_name(suite)(
            self.app,
            block_timeout=block_timeout,
        ).run(names, **options)

    def get_options(self):
        return (
            Option('-i', '--iterations', type='int', default=50,
                   help='Number of iterations for each test'),
            Option('-n', '--numtests', type='int', default=None,
                   help='Number of tests to execute'),
            Option('-o', '--offset', type='int', default=0,
                   help='Start at custom offset'),
            Option('--block-timeout', type='int', default=30 * 60),
            Option('-l', '--list', action='store_true', dest='list_all',
                   help='List all tests'),
            Option('-r', '--repeat', type='float', default=0,
                   help='Number of times to repeat the test suite'),
            Option('-g', '--group', default='all',
                   help='Specify test group (all|green|redis)'),
            Option('--diag', default=False, action='store_true',
                   help='Enable diagnostics (slow)'),
            Option('-J', '--no-join', default=False, action='store_true',
                   help='Do not wait for task results'),
            Option('-S', '--suite',
                   default='cyanide.suites.default:Default',
                   help='Specify test suite to execute (path to class)'),
        )


def main(argv=None):
    return cyanide(app='cyanide.app:app').execute_from_commandline(argv=argv)


if __name__ == '__main__':
    main()