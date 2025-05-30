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

import os

from typ import test_case


class TestDirectories(test_case.TestCase):
    def test_chromium_build_directory(self):
        if not self.is_under_typ:
            self.skipTest('Must be run with typ')
            return
        if not self.chromium_build_directory:
            self.skipTest('--chromium-build-directory not set')
            return

        d = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                         '..', '..', 'tools'))
        self.assertEqual(self.chromium_build_directory, d)
        self.assertEqual(self.chromium_build_directory,
                         os.environ['CHROMIUM_BUILD_DIRECTORY'])

    def test_starting_directory(self):
        if not self.is_under_typ:
            self.skipTest('Must be run with typ')
            return
        if not self.child.starting_directory:
            self.skipTest('only makes sense when --starting-directory is set')
            return

        self.assertEqual(os.getcwd(),
                         os.path.abspath(os.path.dirname(__file__)))


class TestFuncs(test_case.MainTestCase):

    def test_convert_newlines(self):
        cn = test_case.convert_newlines
        self.assertEqual(cn('foo'), 'foo')
        self.assertEqual(cn('foo\nbar\nbaz'), 'foo\nbar\nbaz')
        self.assertEqual(cn('foo\rbar\nbaz\r'), 'foo\nbar\nbaz\n')
        self.assertEqual(cn('foo\r\nbar\r\nbaz\r\nmeh\n'),
                         'foo\nbar\nbaz\nmeh\n')


class TestMainTestCase(test_case.MainTestCase):
    typ_is_required = False

    def test_basic(self):
        h = self.make_host()
        files = {
            'test.py': """
import os
import sys
sys.stdout.write("in: %s\\n" % sys.stdin.read())
sys.stdout.write("out: %s\\n" % os.environ['TEST_VAR'])
sys.stderr.write("err\\n")
with open("../results", "w") as fp:
  fp.write(open("../input", "r").read() + " written")
""",
            'input': 'results',
            'subdir/x': 'y',
        }
        exp_files = files.copy()
        exp_files['results'] = 'results written'
        self.check(prog=[h.python_interpreter, '../test.py'],
                   stdin='hello on stdin',
                   env={'TEST_VAR': 'foo'},
                   cwd='subdir',
                   files=files,
                   ret=0, out='in: hello on stdin\nout: foo\n',
                   err='err\n', exp_files=exp_files)
