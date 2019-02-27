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
from gitinspector.gitinspector import Runner, FileWriter, filtering, interval, __parse_arguments__


class PelicanRepositoryTest(unittest.TestCase):

    def setUp(self):
        # Lowering artificially the threshold of cyclomatic complexity
        # density to trigger it within this test.
        import gitinspector.metrics
        gitinspector.metrics.METRIC_CYCLOMATIC_COMPLEXITY_DENSITY_THRESHOLD = 0.15

        zip_ref = zipfile.ZipFile("tests/resources/pelican-repository.zip", 'r')
        zip_ref.extractall("build/tests")
        zip_ref.close()

    def tearDown(self):
        # TODO: We definitely need to rewrite the 'filtering' and the
        # 'interval' modules to be part of the Runner context and NOT
        # BEING GLOBAL! (for our own sake!)...

        filtering.clear()
        interval.__since__ = ""
        interval.__until__ = ""
        shutil.rmtree("build/tests/pelican-repository")

    def test_process(self):
        # Set options
        opts = __parse_arguments__(args=['--grading', '--legacy',
                                         '--file-types', '*.py',
                                         '--silent',
                                         'build/tests/pelican-repository'])
        opts.progress = False

        # Launch runner
        r = Runner(opts, None)
        r.process()

    def test_output_text(self):
        # Set options
        opts = __parse_arguments__(args=['--grading', '--legacy',
                                         '--file-types', '*.py',
                                         '--format', 'text',
                                         'build/tests/pelican-repository'])
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
                                         '--file-types', '*.py',
                                         '--format', 'html',
                                         'build/tests/pelican-repository'])
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

    def test_output_htmlembedded(self):
        # Set options
        opts = __parse_arguments__(args=['--grading', '--legacy',
                                         '--file-types', '*.py',
                                         '--format', 'htmlembedded',
                                         'build/tests/pelican-repository'])
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
                                         '--file-types', '*.py',
                                         '--format', 'xml',
                                         'build/tests/pelican-repository'])
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
                                         '--file-types', '*.py',
                                         '--format', 'json',
                                         'build/tests/pelican-repository'])
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
