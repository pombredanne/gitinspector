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

from gitinspector.gitinspector import Runner, FileWriter, filtering, interval, __parse_arguments__


class MetricsTest(unittest.TestCase):

    def setUp(self):
        zip_ref = zipfile.ZipFile("tests/resources/trie-repository.zip", 'r')
        zip_ref.extractall("build/tests")
        zip_ref.close()

    def tearDown(self):
        pass

    def test_all_changes(self):
        opts = __parse_arguments__(args=['--silent',
                                         'build/tests/trie-repository'])
        opts.progress = False

        # Launch runner
        r = Runner(opts, None)
        r.process()
        self.assertEqual(len(r.changes.commits), 29)  # 29 commits + 2 merges
        b_commits = [c for c in r.changes.commits if c.author == "Bilbo Baggins"]
        self.assertEqual(len(b_commits), 11)  # 11 commits + 1 merge
        f_commits = [c for c in r.changes.commits if c.author == "Frodo Baggins"]
        self.assertEqual(len(f_commits), 6)   # 6 commits
        s_commits = [c for c in r.changes.commits if c.author == "Samwise Gamgee"]
        self.assertEqual(len(s_commits), 6)   # 6 commits + 1 merge

    def test_small_changes(self):
        opts = __parse_arguments__(args=['--silent', '--since=2015-10-20', '--until=2015-10-22',
                                         'build/tests/trie-repository'])
        opts.progress = False

        # Launch runner
        r = Runner(opts, None)
        r.process()
        self.assertEqual(len(r.changes.commits), 4)  # 4 commits + 1 merge
        b_commits = [c for c in r.changes.commits if c.author == "Bilbo Baggins"]
        self.assertEqual(len(b_commits), 3)  # 3 commits + 1 merge
        f_commits = [c for c in r.changes.commits if c.author == "Frodo Baggins"]
        self.assertEqual(len(f_commits), 0)  # 0 commits
        s_commits = [c for c in r.changes.commits if c.author == "Samwise Gamgee"]
        self.assertEqual(len(s_commits), 1)  # 1 commits
