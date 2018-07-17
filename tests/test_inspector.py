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
# dir
class RepositoryTest(unittest.TestCase):
    def test(self):
        r = Runner()
        zip_ref = zipfile.ZipFile("tests/resources/repository.zip", 'r')
        zip_ref.extractall("build/tests")
        zip_ref.close()
        repos = __get_validated_git_repos__(["build/tests/repository"])
        extensions.define("c,txt")
        r.process(repos)
