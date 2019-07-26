# coding: utf-8
#
# This file is part of gitinspector.
#
# gitinspector is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gitinspector is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gitinspector. If not, see <http://www.gnu.org/licenses/>.

import hashlib
import locale
import os
import shutil
import tempfile
import unittest
import zipfile

import gitinspector.localization as localization
from gitinspector.gitinspector import Runner, FileWriter, filtering, interval, StdoutWriter, __parse_arguments__


class TrieRepositoryTest(unittest.TestCase):

    def setUp(self):
        zip_ref = zipfile.ZipFile("tests/resources/trie-repository.zip", 'r')
        zip_ref.extractall("build/tests")
        zip_ref.close()

    def tearDown(self):
        shutil.rmtree("build/tests/trie-repository")

    def test_process(self):
        # Set options
        opts = __parse_arguments__(args=['--grading', '--legacy',
                                         '--file-types', '*.c,*.h',
                                         '--silent',
                                         'build/tests/trie-repository'])
        opts.progress = False

        # Launch runner
        r = Runner(opts, None)
        r.process()

    def test_output_text(self):
        # Set options
        opts = __parse_arguments__(args=['--grading', '--legacy',
                                         '--file-types', '*.c,*.h',
                                         '--format', 'text',
                                         'build/tests/trie-repository'])
        opts.progress = False

        # Launch runner
        localization.init_null()
        file = tempfile.NamedTemporaryFile('w', delete=False)
        r = Runner(opts, FileWriter(file))
        r.process()
        with open(file.name, 'r') as f:
            contents = f.read()
            self.assertTrue("Statistical information" in contents)
            self.assertTrue("The following historical commit" in contents)
            self.assertTrue("Below are the number of rows" in contents)
            self.assertTrue("The following history timeline" in contents)
        os.remove(file.name)

    def test_output_html(self):
        # Set options
        opts = __parse_arguments__(args=['--grading', '--legacy',
                                         '--file-types', '*.c,*.h',
                                         '--format', 'html',
                                         'build/tests/trie-repository'])
        opts.progress = False

        # Launch runner
        localization.init_null()
        file = tempfile.NamedTemporaryFile('w', delete=False)
        r = Runner(opts, FileWriter(file))
        r.process()
        with open(file.name, 'r') as f:
            contents = f.read()
            self.assertTrue("Statistical information" in contents)
            self.assertTrue("The following history timeline" in contents)
        os.remove(file.name)

    def test_output_xml(self):
        # Set options
        opts = __parse_arguments__(args=['--grading', '--legacy',
                                         '--file-types', '*.c,*.h',
                                         '--format', 'xml',
                                         'build/tests/trie-repository'])
        opts.progress = False

        # Launch runner
        localization.init_null()
        file = tempfile.NamedTemporaryFile('w', delete=False)
        r = Runner(opts, FileWriter(file))
        r.process()
        with open(file.name, 'r') as f:
            contents = f.read()
            self.assertTrue("The following historical commit" in contents)
            self.assertTrue("Below are the number of rows" in contents)
            self.assertTrue("The following history timeline" in contents)
        os.remove(file.name)

    def test_output_json(self):
        # Set options
        opts = __parse_arguments__(args=['--grading', '--legacy',
                                         '--file-types', '*.c,*.h',
                                         '--format', 'json',
                                         'build/tests/trie-repository'])
        opts.progress = False

        # Launch runner
        localization.init_null()
        file = tempfile.NamedTemporaryFile('w', delete=False)
        r = Runner(opts, FileWriter(file))
        r.process()
        with open(file.name, 'r') as f:
            contents = f.read()
            self.assertTrue("The following historical commit" in contents)
            self.assertTrue("Below are the number of rows" in contents)
            self.assertTrue("The following history timeline" in contents)
        os.remove(file.name)
