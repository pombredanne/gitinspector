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
import unittest
import zipfile
from gitinspector.gitinspector import Runner, __get_validated_git_repos__
import gitinspector.extensions as extensions

# Test gitinspector over a git repository present in the resources/
# dir, count the changes and the blames and check the metrics. 
class RepositoryTest(unittest.TestCase):
    def test(self):
        r = Runner()
        zip_ref = zipfile.ZipFile("tests/resources/repository.zip", 'r')
        zip_ref.extractall("build/tests")
        zip_ref.close()
        repos = __get_validated_git_repos__(["build/tests/repository"])
        extensions.define("c,txt")
        r.include_metrics = True
        r.process(repos, silent = True)
        # Chack the repositories
        self.assertEqual(len(r.repos), 1)
        self.assertEqual(r.repos[0].name, "repository")
        self.assertTrue(r.repos[0].location.endswith("build/tests/repository"))
        # Check the commits
        self.assertEqual(len(r.changes.commits), 2)
        self.assertEqual(r.changes.commits[0].author, "Abraham Lincoln")
        self.assertEqual(r.changes.commits[1].author, "Andrew Johnson")
        # Check the blames
        self.assertEqual(len(r.blames.blames.keys()), 2)
        blame_keys = list(r.blames.blames.keys())
        self.assertEqual(blame_keys[0], ('Abraham Lincoln', 'README.txt'))
        self.assertEqual(blame_keys[1], ('Andrew Johnson', 'file.c'))
        self.assertEqual(r.blames.blames[blame_keys[0]].rows, 1) # README.txt is 1 line long
        self.assertEqual(r.blames.blames[blame_keys[1]].rows, 6) # main.c     is 6 lines long
        # Check the metrics
        self.assertEqual(r.metrics.eloc, {}) # Both files are too short, no metrics to report
