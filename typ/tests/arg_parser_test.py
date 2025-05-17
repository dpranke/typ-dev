# Copyright 2014 Dirk Pranke. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import optparse
import unittest

from typ import ArgumentParser
from typ.fakes.host_fake import FakeHost


class ArgumentParserTest(unittest.TestCase):

    def test_optparse_options(self):
        parser = optparse.OptionParser()
        ArgumentParser.add_option_group(parser, 'foo',
                                        discovery=True,
                                        running=True,
                                        reporting=True,
                                        skip='[-d]')
        options, _ = parser.parse_args(['-j', '1'])
        self.assertEqual(options.jobs, 1)

    def test_argv_from_args(self):
        def check(argv, expected):
            parser = ArgumentParser(host=FakeHost())
            args = parser.parse_args(argv)
            actual_argv = parser.argv_from_args(args)
            self.assertEqual(expected, actual_argv)

        check(
            ['--version'],
            [
                '--no-overwrite',
                '--no-print-start-time',
                '--no-print-workers',
                '--version',
            ]
        )
        check(
            ['--coverage', '--coverage-omit', 'foo'],
            [
                '--coverage',
                '--coverage-omit',
                'foo',
                '--no-overwrite',
                '--no-print-start-time',
                '--no-print-workers',
            ]
        )
        check(
            ['--jobs', '3'],
            [
                '--jobs', '3',
                '--no-overwrite',
                '--no-print-start-time',
                '--no-print-workers',
            ]
        )
        check(
            ['-vv'],
            [
                '--no-overwrite',
                '--print-start-time',
                '--print-workers',
                '--verbose',
                '--verbose',
            ]
        )

    def test_argv_from_args_foreign_argument(self):
        host = FakeHost()
        parser = ArgumentParser(host=host)
        parser.add_argument('--some-foreign-argument', default=False,
                            action='store_true')
        args = parser.parse_args(['--some-foreign-argument', '--verbose'])
        self.assertEqual(
            [
                '--no-overwrite',
                '--print-start-time',
                '--print-workers',
                '--verbose',
            ],
            ArgumentParser(host=host).argv_from_args(args))

    def test_valid_shard_options(self):
        parser = ArgumentParser()

        parser.parse_args(['--total-shards', '1'])
        self.assertEqual(parser.exit_status, None)

        parser.parse_args(['--total-shards', '5', '--shard-index', '4'])
        self.assertEqual(parser.exit_status, None)

        parser.parse_args(['--total-shards', '5', '--shard-index', '0'])
        self.assertEqual(parser.exit_status, None)

    def test_invalid_shard_options(self):
        parser = ArgumentParser(host=FakeHost())

        parser.parse_args(['--total-shards', '0'])
        self.assertEqual(parser.exit_status, 2)

        parser.parse_args(['--total-shards', '-1'])
        self.assertEqual(parser.exit_status, 2)

        parser.parse_args(['--total-shards', '5', '--shard-index', '-1'])
        self.assertEqual(parser.exit_status, 2)

        parser.parse_args(['--total-shards', '5', '--shard-index', '5'])
        self.assertEqual(parser.exit_status, 2)

        parser.parse_args(['--total-shards', '5', '--shard-index', '6'])
        self.assertEqual(parser.exit_status, 2)
