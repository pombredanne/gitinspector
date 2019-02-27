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


class CommandLineOptionsTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        # TODO: We definitely need to rewrite the 'filtering' and the
        # 'interval' modules to be part of the Runner context and NOT
        # BEING GLOBAL! (for our own sake!)...
        filtering.clear()
        interval.__since__ = ""
        interval.__until__ = ""

    def test_help(self):
        # Set options
        import sys
        from io import StringIO
        from gitinspector.gitinspector import main

        # Setting a fake sys.argv and ssys.stdout
        argv_orig = sys.argv
        stdout_orig = sys.stdout
        sys.stdout = custom_stdout = StringIO()

        # Running the software on '--help'
        sys.argv = ['./gitinspector.py', '--help']
        try:
            main()
        except SystemExit:
            self.assertTrue(sys.stdout)

        # Restoring the original context
        sys.argv = argv_orig
        sys.stdout.close()
        sys.stdout = stdout_orig

    def test_version(self):
        # Set options
        import sys
        from io import StringIO
        from gitinspector.gitinspector import main

        # Setting a fake sys.argv and ssys.stdout
        argv_orig = sys.argv
        stdout_orig = sys.stdout
        sys.stdout = custom_stdout = StringIO()

        # Running the software on '--version'
        sys.argv = ['./gitinspector.py', '--version']
        try:
            main()
        except SystemExit:
            self.assertTrue(sys.stdout)

        # Restoring the original context
        sys.argv = argv_orig
        sys.stdout.close()
        sys.stdout = stdout_orig

    def test_repository_analysis(self):
        # Set options
        import sys
        from io import StringIO
        from gitinspector.gitinspector import main

        # Setting a fake sys.argv and sys.stdout
        argv_orig = sys.argv
        stdout_orig = sys.stdout
        sys.stdout = custom_stdout = StringIO()

        # Extracting the repository
        zip_ref = zipfile.ZipFile("tests/resources/basic-repository.zip", 'r')
        zip_ref.extractall("build/tests")
        zip_ref.close()

        # Running the software
        sys.argv = ['gitinspector.py', 'build/tests/basic-repository']
        main()
        self.assertTrue(sys.stdout)

        # Restoring the original context
        sys.argv = argv_orig
        sys.stdout.close()
        sys.stdout = stdout_orig
        shutil.rmtree("build/tests/basic-repository")
