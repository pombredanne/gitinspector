# coding: utf-8
#
# Copyright © 2018-2019 David Renault. All rights reserved.
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

import itertools
import subprocess


def local_branches():
    """Returns the list of branches appearing as local references.
    """
    branch_p = subprocess.Popen(["git", "branch", "--format=%(refname)"], bufsize=1,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    branches = branch_p.communicate()[0].splitlines()
    branches = [ b.decode("utf-8", "replace") for b in branches ]
    branches = [ b for b in branches if b.startswith("refs") ] # Filter detached HEADs
    branch_p.wait()
    branch_p.stdout.close()
    return branches


def last_commit(branch, file):
    """Returns the date for the last commit on a file in a branch, in the
       Unix format, 0 if the file does not belong to the branch.
    """
    log_p = subprocess.Popen(["git", "log", "-1", "--format=%at", branch, file], bufsize=1,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    date_s = log_p.communicate()[0].strip().decode("utf-8")
    try:
        date = int(date_s)
    except ValueError:
        date = 0
    log_p.wait()
    log_p.stdout.close()
    return date


def sanitize_filename(file):
    file = file.strip().decode("unicode_escape", "ignore")
    file = file.encode("latin-1", "replace")
    file = file.decode("utf-8", "replace").strip("\"").strip("'").strip()
    return file


def files(branch, config):
    """Returns the list of the files appearing in the given branch.
    """
    ls_command = ["git", "ls-tree", "--name-only", "-r", branch]

    if config.debug_mode:
        print(" ".join(ls_command))

    ls_tree_p = subprocess.Popen(ls_command, bufsize=1,
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lines = ls_tree_p.communicate()[0].splitlines()
    lines = [ sanitize_filename(l) for l in lines ]
    ls_tree_p.wait()
    ls_tree_p.stdout.close()
    return lines


def commits(branch, since, until):
    """Returns a list of SHA for the commits in the given branch, for the
    given duration.
    """
    git_command = filter(None, ["git", "rev-list", "--reverse", # "--no-merges", # For oavsa
                                since, until, branch])
    git_rev_list_p = subprocess.Popen(git_command, bufsize=1,
                                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lines = git_rev_list_p.communicate()[0].splitlines()
    git_rev_list_p.wait()
    git_rev_list_p.stdout.close()
    return lines


def commit_chunks(hashes, since, until, config):
    """Returns a list of commits containing the commit data with the
    filediffs. Returned is a list of chunks, each chunk being one
    commit represented by a list of lines. The return of this function
    is intended to be handled by Commit.handle_diff_chunk.
    """
    git_command = list(filter(None,
                         ["git", "log", "--reverse",
                          "--pretty='---%n%ct|%cd|%H|%aN|%aE'",
                          "--stat=100000,8192"] +
                         (["-w"] if config.ignore_space else []) +
                         [since, until, "--date=short"] +
                         (["-C", "-C", "-M"] if config.hard else []) +
                         [hashes]))
    git_command = " ".join(git_command)
    if config.debug_mode:
        print(git_command)

    git_log_r = subprocess.Popen(git_command,
                                 bufsize=1, stdout=subprocess.PIPE, shell=True)
    lines = git_log_r.stdout.readlines()
    git_log_r.wait()
    git_log_r.stdout.close()
    chunks = [ list(g) for (k,g) in itertools.groupby(lines, key=lambda l: l==b'---\n') ]
    chunks = list(filter(lambda g: g[0] != b'---\n', chunks))
    return chunks


def commit_message(hash):
    """Returns the commit message of a given hash, as a list of strings"""
    git_command = filter(None, ["git", "show", "-s",
                                "--pretty=%B", hash])
    git_show_r = subprocess.Popen(git_command, bufsize=1, stdout=subprocess.PIPE)
    message = git_show_r.stdout.read() # all lines in one go
    git_show_r.wait()
    git_show_r.stdout.close()

    message = message.strip().decode("unicode_escape", "ignore")
    message = message.encode("latin-1", "replace")
    return message.decode("utf-8", "replace")


def blames(sha, filename, config):
    """Returns a list of data representing the blames for a file on a
    given branch.
    """
    blame_command = list(filter(None,
                           ["git", "blame", "--line-porcelain"] +
                           (["-w"] if config.ignore_space else []) +
                           (["-C", "-C", "-M"] if config.hard else []) +
                           [sha, "--", filename]))
    blame_command = " ".join(blame_command)
    if config.debug_mode:
        print(blame_command)

    git_blame_cmd = subprocess.Popen(blame_command, bufsize=1, shell=True,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    rows = git_blame_cmd.stdout.readlines()
    git_blame_cmd.wait()
    git_blame_cmd.stdout.close()
    git_blame_cmd.stderr.close()
    return rows


def config(repo, variable, global_only):
    """Returns the value of a variable configured in a repository.
    """
    setting_cmd = subprocess.Popen(filter(None, ["git", "-C", repo, "config",
                                                 "--global" if global_only else "",
                                                 "inspector." + variable]), bufsize=1,
                                   stdout=subprocess.PIPE)
    setting_cmd.wait()

    try:
        setting = setting_cmd.stdout.readlines()[0].strip().decode("utf-8", "replace")
    except IndexError:
        setting = ""

    setting_cmd.stdout.close()
    return setting
