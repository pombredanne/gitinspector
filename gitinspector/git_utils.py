# coding: utf-8
#
# Copyright © 2012-2017 Ejwa Software. All rights reserved.
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

import subprocess

def local_branches():
    branch_p = subprocess.Popen(["git", "branch", "--format=%(refname)"], bufsize=1,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    branches = branch_p.communicate()[0].splitlines()
    branch_p.wait()
    branch_p.stdout.close()
    return branches

def last_commit(branch, file):
    """Returns the date for the last commit on a file in a branch, in the
       Unix format.
    """
    log_p = subprocess.Popen(["git", "log", "-1", "--format=%at", branch, file], bufsize=1,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    date = int(log_p.communicate()[0].strip().decode("utf-8"))
    log_p.wait()
    log_p.stdout.close()
    return date

def sanitize_filename(file):
    file = file.strip().decode("unicode_escape", "ignore")
    file = file.encode("latin-1", "replace")
    file = file.decode("utf-8", "replace").strip("\"").strip("'").strip()
    return file

def files(branch):
    """Returns the list of the files in the given branch.
    """
    ls_tree_p = subprocess.Popen(["git", "ls-tree", "--name-only", "-r",
                                  branch], bufsize=1,
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lines = ls_tree_p.communicate()[0].splitlines()
    lines = [ sanitize_filename(l) for l in lines ]
    ls_tree_p.wait()
    ls_tree_p.stdout.close()
    return lines

def commits(branch, since, until):
    git_command = filter(None, ["git", "rev-list", "--reverse", # "--no-merges", # For oavsa
                                since, until, branch])
    git_rev_list_p = subprocess.Popen(git_command, bufsize=1,
                                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lines = git_rev_list_p.communicate()[0].splitlines()
    git_rev_list_p.wait()
    git_rev_list_p.stdout.close()
    return lines
