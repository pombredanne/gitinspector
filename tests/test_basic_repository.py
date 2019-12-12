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

import os
import shutil
import tempfile
import unittest
import zipfile

import gitinspector.localization as localization
from gitinspector.gitinspector import Runner, FileWriter, __parse_arguments__


# Test gitinspector over a git repository present in the resources/
# dir, count the changes and the blames and check the metrics.
class BasicRepositoryTest(unittest.TestCase):

    def setUp(self):
        zip_ref = zipfile.ZipFile("tests/resources/basic-repository.zip", 'r')
        zip_ref.extractall("build/tests")
        zip_ref.close()

    def tearDown(self):
        shutil.rmtree("build/tests/basic-repository")

    def test_process(self):
        # Set options
        opts = __parse_arguments__(args=['--grading', '--legacy',
                                         '--branch', 'master',
                                         '--file-types', '*.c,*.txt,Makefile',
                                         '--exclude', 'author:John Doe',
                                         '--silent',
                                         'build/tests/basic-repository'])
        opts.progress = False

        # Launch runner
        r = Runner(opts, None)
        r.process()

        # Check the repositories
        self.assertEqual(len(r.repos), 1)
        self.assertEqual(r.repos[0].name, "basic-repository")
        self.assertTrue(r.repos[0].location.endswith("build/tests/basic-repository"))
        authors = r.repos[0].authors()
        authors.sort()
        self.assertEqual(authors,
                         ['Abraham Lincoln <abe@gov.us>', 'Andrew Johnson <jojo@gov.us>'])

        # Check the commits
        self.assertEqual(len(r.changes.all_commits()), 4)
        authors = sorted(list(map(lambda c: c.author, r.changes.all_commits())))
        self.assertEqual(authors[0], "Abraham Lincoln")
        self.assertEqual(authors[1], "Andrew Johnson")

        # Check the blames
        blames = r.blames.all_blames()
        self.assertEqual(len(blames.keys()), 3)
        blame_keys = sorted(list(blames.keys()))
        self.assertEqual(blame_keys[0], (('Abraham Lincoln', 'abe@gov.us'), 'README.txt'))
        self.assertEqual(blame_keys[1], (('Andrew Johnson', 'jojo@gov.us'), 'Makefile'))
        self.assertEqual(blame_keys[2], (('Andrew Johnson', 'jojo@gov.us'), 'file.c'))
        self.assertEqual(blames[blame_keys[0]].rows, 1)  # README.txt is 1 line long
        self.assertEqual(blames[blame_keys[1]].rows, 10) # Makefile   is 10 lines long
        self.assertEqual(blames[blame_keys[2]].rows, 40) # file.c     is 40 lines long

        # Check the metrics
        self.assertEqual(r.metrics.eloc, {}) # Both files are too short, no metrics to report

    def test_output_text(self):
        # Set options
        opts = __parse_arguments__(args=['--grading', '--legacy',
                                         '--file-types', '*.c,*.txt',
                                         '--exclude', 'author:John Doe',
                                         '--format', 'text',
                                         'build/tests/basic-repository'])
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
        os.remove(file.name)

    def test_output_html(self):
        # Set options
        opts = __parse_arguments__(args=['--grading', '--legacy',
                                         '--file-types', '*.c,*.txt',
                                         '--exclude', 'author:John Doe',
                                         '--format', 'html',
                                         'build/tests/basic-repository'])
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
                                         '--file-types', '*.c,*.txt',
                                         '--exclude', 'author:John Doe',
                                         '--format', 'xml',
                                         'build/tests/basic-repository'])
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
                                         '--file-types', '*.c,*.txt',
                                         '--exclude', 'author:John Doe',
                                         '--format', 'json',
                                         'build/tests/basic-repository'])
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


# Test gitinspector over a git repository present in the resources/
# dir, count the changes and the blames and check the metrics. These
# tests are a bit different because they add some exclusion filters.
class BasicFilteredRepositoryTest(unittest.TestCase):

    def setUp(self):
        zip_ref = zipfile.ZipFile("tests/resources/basic-repository.zip", 'r')
        zip_ref.extractall("build/tests")
        zip_ref.close()

    def tearDown(self):
        shutil.rmtree("build/tests/basic-repository")

    def test_process(self):
        # Set options
        opts = __parse_arguments__(args=['--grading', '--legacy',
                                         '--branch', 'master',
                                         '--file-types', '*.c,*.txt,Make*',
                                         '--exclude', 'author:Abraham Lincoln,file_out:Makefile',
                                         '--since', '2001-01-01',
                                         '--until', '2020-01-01',
                                         '--silent',
                                         'build/tests/basic-repository'])
        opts.progress = False

        # 1 commit is excluded from the author "Abraham Lincoln"
        # 1 file is filtered because it only applies to the "Makefile"

        # Launch runner
        r = Runner(opts, None)
        r.process()

        # Check the repositories
        self.assertEqual(len(r.repos), 1)
        self.assertEqual(r.repos[0].name, "basic-repository")
        self.assertTrue(r.repos[0].location.endswith("build/tests/basic-repository"))
        authors = r.repos[0].authors()
        authors.sort()
        self.assertEqual(authors,
                         ['Abraham Lincoln <abe@gov.us>', 'Andrew Johnson <jojo@gov.us>'])

        # Check the commits
        rel_commits = r.changes.relevant_commits()
        self.assertEqual(len(rel_commits), 3) # 4 commits, 1 excluded
        all_commits = r.changes.all_commits()
        self.assertEqual(len(all_commits), 4) # 4 commits, 1 excluded
        authors = sorted(list(map(lambda c: c.author, rel_commits)))
        self.assertEqual(authors[0], "Andrew Johnson")

        filtered_files = r.changes.filtered_files(('Andrew Johnson', 'jojo@gov.us'))
        self.assertEqual(len(filtered_files), 1)
        self.assertEqual(list(filtered_files)[0], "Makefile")

        # Check the blames
        blames = r.blames.all_blames()
        self.assertEqual(len(blames.keys()), 1)
        blame_keys = sorted(list(blames.keys()))
        self.assertEqual(blame_keys[0], (('Andrew Johnson', 'jojo@gov.us'), 'file.c'))
        self.assertEqual(blames[blame_keys[0]].rows, 40) # file.c is 40 lines long

        # Check the metrics
        self.assertEqual(r.metrics.eloc, {}) # Both files are too short, no metrics to report

    def test_output_text(self):
        # Set options
        opts = __parse_arguments__(args=['--grading', '--legacy',
                                         '--file-types', '*.c,*.txt',
                                         '--exclude', 'author:Abraham Lincoln',
                                         '--since', '2001-01-01',
                                         '--until', '2020-01-01',
                                         '--format', 'text',
                                         'build/tests/basic-repository'])
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
                                         '--file-types', '*.c,*.txt',
                                         '--exclude', 'author:Abraham Lincoln',
                                         '--since', '2001-01-01',
                                         '--until', '2020-01-01',
                                         '--format', 'html',
                                         'build/tests/basic-repository'])
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
                                         '--file-types', '*.c,*.txt',
                                         '--exclude', 'author:Abraham Lincoln',
                                         '--since', '2001-01-01',
                                         '--until', '2020-01-01',
                                         '--format', 'xml',
                                         'build/tests/basic-repository'])
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
                                         '--file-types', '*.c,*.txt',
                                         '--exclude', 'author:Abraham Lincoln',
                                         '--since', '2001-01-01',
                                         '--until', '2020-01-01',
                                         '--format', 'json',
                                         'build/tests/basic-repository'])
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
