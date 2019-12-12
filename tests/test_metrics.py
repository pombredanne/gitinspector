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

import shutil
import unittest
import zipfile


from gitinspector.gitinspector import Runner, __parse_arguments__
from gitinspector.changes import CommitType


# Test the metrics on the basic repository, a very simple repository
# with no merge and two branches
class MetricsBasicTest(unittest.TestCase):

    def setUp(self):
        zip_ref = zipfile.ZipFile("tests/resources/basic-repository.zip", 'r')
        zip_ref.extractall("build/tests")
        zip_ref.close()

    def tearDown(self):
        shutil.rmtree("build/tests/basic-repository")

    def test_all_changes(self):
        opts = __parse_arguments__(args=['--silent',
                                         'build/tests/basic-repository'])
        opts.progress = False

        # Launch runner
        r = Runner(opts, None)
        r.process()

        # Test number of commits
        self.assertEqual(len(r.changes.all_commits()), 6)  # 6 commits, no merges
        self.assertEqual(len(r.changes.relevant_commits()), 6)
        self.assertEqual(len(r.changes.merge_commits()), 0)
        l_commits = [c for c in r.changes.all_commits() if c.author == "Abraham Lincoln"]
        self.assertEqual(len(l_commits), 3)  # 3 commits
        j_commits = [c for c in r.changes.all_commits() if c.author == "Andrew Johnson"]
        self.assertEqual(len(l_commits), 3)  # 3 commits

        # Test insertions and deletions
        authorinfos = r.changes.get_authorinfo_list()
        self.assertEqual(len(authorinfos), 2) # 2 authors
        abe_commits = authorinfos[('Abraham Lincoln', 'abe@gov.us')]
        self.assertEqual(abe_commits.commits, 3)
        self.assertEqual(abe_commits.insertions, 28) # 10 + 17 + 1
        self.assertEqual(abe_commits.deletions, 0)
        and_commits = authorinfos[('Andrew Johnson', 'jojo@gov.us')]
        self.assertEqual(and_commits.commits, 3)
        self.assertEqual(and_commits.insertions, 50) # 10 + 34 + 6
        self.assertEqual(and_commits.deletions, 0)

    def test_master_changes(self):
        opts = __parse_arguments__(args=['--silent',
                                         '--branch', 'master',
                                         'build/tests/basic-repository'])
        opts.progress = False

        # Launch runner
        r = Runner(opts, None)
        r.process()

        # Test number of commits
        self.assertEqual(len(r.changes.all_commits()), 4)  # 4 commits, no merges
        self.assertEqual(len(r.changes.relevant_commits()), 4)
        self.assertEqual(len(r.changes.merge_commits()), 0)
        l_commits = [c for c in r.changes.all_commits() if c.author == "Abraham Lincoln"]
        self.assertEqual(len(l_commits), 1)  # 1 commits
        j_commits = [c for c in r.changes.all_commits() if c.author == "Andrew Johnson"]
        self.assertEqual(len(j_commits), 3)  # 3 commits

        # Test insertions and deletions
        authorinfos = r.changes.get_authorinfo_list()
        self.assertEqual(len(authorinfos), 2) # 2 authors
        abe_commits = authorinfos[('Abraham Lincoln', 'abe@gov.us')]
        self.assertEqual(abe_commits.commits, 1)
        self.assertEqual(abe_commits.insertions, 1) # 1
        self.assertEqual(abe_commits.deletions, 0)
        and_commits = authorinfos[('Andrew Johnson', 'jojo@gov.us')]
        self.assertEqual(and_commits.commits, 3)
        self.assertEqual(and_commits.insertions, 50) # 10 + 34 + 6
        self.assertEqual(and_commits.deletions, 0)


# Test the metrics on the trie repository, a fairly simple repository
# with some merges
class MetricsTrieTest(unittest.TestCase):

    def setUp(self):
        zip_ref = zipfile.ZipFile("tests/resources/trie-repository.zip", 'r')
        zip_ref.extractall("build/tests")
        zip_ref.close()

    def tearDown(self):
        shutil.rmtree("build/tests/trie-repository")

    def test_all_changes(self):
        opts = __parse_arguments__(args=['--silent',
                                         'build/tests/trie-repository'])
        opts.progress = False

        # Launch runner
        r = Runner(opts, None)
        r.process()

        # Test number of commits
        self.assertEqual(len(r.changes.all_commits()), 31)  # 29 commits + 2 merges
        self.assertEqual(len(r.changes.code_commits()), 29)
        self.assertEqual(len(r.changes.merge_commits()), 2)
        b_commits = [c for c in r.changes.all_commits() if c.author == "Bilbo Baggins"]
        self.assertEqual(len(b_commits), 12)  # 11 commits + 1 merge
        self.assertEqual(len([c for c in b_commits if c.type == CommitType.CODE]), 11)
        self.assertEqual(len([c for c in b_commits if c.type == CommitType.MERGE]), 1)
        f_commits = [c for c in r.changes.all_commits() if c.author == "Frodo Baggins"]
        self.assertEqual(len(f_commits), 6)   # 6 commits
        s_commits = [c for c in r.changes.all_commits() if c.author == "Samwise Gamgee"]
        self.assertEqual(len(s_commits), 7)   # 6 commits + 1 merge
        self.assertEqual(len([c for c in s_commits if c.type == CommitType.CODE]), 6)

        # Test insertions and deletions
        authorinfos = r.changes.get_authorinfo_list()
        self.assertEqual(len(authorinfos), 5) # 5 authors

    def test_small_changes(self):
        opts = __parse_arguments__(args=['--silent', '--since=2015-10-20', '--until=2015-10-22',
                                         'build/tests/trie-repository'])
        opts.progress = False

        # Launch runner
        r = Runner(opts, None)

        # Test number of commits
        r.process()
        self.assertEqual(len(r.changes.all_commits()), 5)  # 4 commits + 1 merge
        self.assertEqual(len(r.changes.code_commits()), 4)
        self.assertEqual(len(r.changes.merge_commits()), 1)
        b_commits = [c for c in r.changes.all_commits() if c.author == "Bilbo Baggins"]
        self.assertEqual(len(b_commits), 4)  # 3 commits + 1 merge
        self.assertEqual(len([c for c in b_commits if c.type == CommitType.CODE]), 3)
        self.assertEqual(len([c for c in b_commits if c.type == CommitType.MERGE]), 1)
        f_commits = [c for c in r.changes.all_commits() if c.author == "Frodo Baggins"]
        self.assertEqual(len(f_commits), 0)  # 0 commits
        s_commits = [c for c in r.changes.all_commits() if c.author == "Samwise Gamgee"]
        self.assertEqual(len(s_commits), 1)  # 1 commits

        # Test insertions and deletions
        authorinfos = r.changes.get_authorinfo_list()
        bilbo_commits = authorinfos[('Bilbo Baggins', 'bilbo.baggins@shire.net')]
        self.assertEqual(bilbo_commits.commits, 4)
        self.assertEqual(bilbo_commits.insertions, 14) # 3 + 7 + 4
        self.assertEqual(bilbo_commits.deletions, 8)   # 4 + 0 + 4
        sam_commits = authorinfos[('Samwise Gamgee', 'samwise.gamgee@shire.net')]
        self.assertEqual(sam_commits.commits, 1)
        self.assertEqual(sam_commits.insertions, 41) # 41 (22+19)
        self.assertEqual(sam_commits.deletions, 0)

    def test_all_blames_without_spaces(self):
        opts = __parse_arguments__(args=['--silent', # '-b', 'master'
                                         'build/tests/trie-repository'])
        opts.progress = False

        # Launch runner
        r = Runner(opts, None)
        r.process()

        # Count the blames in the README
        r_blames = r.blames.blames_for_file("README")
        self.assertEqual(len(r_blames), 1)
        r_blames_1 = r_blames[0]
        self.assertEqual(r_blames_1[0][0], "Frodo Baggins")
        self.assertEqual(r_blames_1[1],    8) # 8 lines from Frodo
        # Count the blames in src/trie.c
        t_blames = r.blames.blames_for_file("src/trie.c")
        self.assertEqual(len(t_blames), 5)    # 5 authors
        t_blames_1 = [ t for t in t_blames if t[0][0] == "Frodo Baggins" ][0]
        self.assertEqual(t_blames_1[1], 40)
        t_blames_2 = [ t for t in t_blames if t[0][0] == "Peregrin Took" ][0]
        self.assertEqual(t_blames_2[1], 64)
        t_blames_3 = [ t for t in t_blames if t[0][0] == "Bilbo Baggins" ][0]
        self.assertEqual(t_blames_3[1], 107)

    def test_all_blames_with_spaces(self):
        opts = __parse_arguments__(args=['--silent', # '-b', 'master'
                                         '-W',
                                         'build/tests/trie-repository'])
        opts.progress = False

        # Launch runner
        r = Runner(opts, None)
        r.process()

        # Count the blames in the README
        r_blames = r.blames.blames_for_file("README")
        self.assertEqual(len(r_blames), 1)
        r_blames_1 = r_blames[0]
        self.assertEqual(r_blames_1[0][0], "Frodo Baggins")
        self.assertEqual(r_blames_1[1],    8) # 8 lines from Frodo
        # Count the blames in src/trie.c
        t_blames = r.blames.blames_for_file("src/trie.c")
        self.assertEqual(len(t_blames), 5)    # 5 authors
        t_blames_1 = [ t for t in t_blames if t[0][0] == "Frodo Baggins" ][0]
        self.assertEqual(t_blames_1[1], 41)
        t_blames_2 = [ t for t in t_blames if t[0][0] == "Peregrin Took" ][0]
        self.assertEqual(t_blames_2[1], 56)
        t_blames_3 = [ t for t in t_blames if t[0][0] == "Bilbo Baggins" ][0]
        self.assertEqual(t_blames_3[1], 109)
