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

import bisect
import copy
import datetime
import multiprocessing
import os
import subprocess
import threading
from .filtering import Filters, is_filtered
from . import format, interval, terminal

CHANGES_PER_THREAD = 200
NUM_THREADS = multiprocessing.cpu_count()

__thread_lock__ = threading.BoundedSemaphore(NUM_THREADS)
__changes_lock__ = threading.Lock()


class AuthorColors(object):

    colors =  [
        "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
        "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
        "#77b41f", "#7f0eff", "#a02c2c", "#2728d6", "#67bd94",
        "#564b8c", "#77c2e3", "#bd22bc", "#becf17",
        "#b41f77", "#0eff7f", "#2c2ca0", "#28d627", "#bd9467",
        "#4b8c56", "#c2e377", "#22bcbd", "#cf17be",
    ]
    index = -1

    @staticmethod
    def get_new_color():
        AuthorColors.index += 1
        return AuthorColors.colors[AuthorColors.index % len(AuthorColors.colors)]


class FileDiff(object):
    def __init__(self, string):
        commit_line = string.split("|")

        if commit_line.__len__() == 2:
            self.name = commit_line[0].strip()
            self.insertions = commit_line[1].count("+")
            self.deletions = commit_line[1].count("-")

    @staticmethod
    def is_filediff_line(string):
        string = string.split("|")
        return string.__len__() == 2 and string[1].find("Bin") == -1 and ('+' in string[1] or '-' in string[1])

    @staticmethod
    def get_extension(string):
        string = string.split("|")[0].strip().strip("{}").strip("\"").strip("'")
        return os.path.splitext(string)[1][1:]

    @staticmethod
    def get_filename(string):
        return string.split("|")[0].strip().strip("{}").strip("\"").strip("'")

    @staticmethod
    def is_valid_extension(string):
        return is_filtered(FileDiff.get_filename(string))


class Commit(object):
    def __init__(self, string, config):
        self.filediffs = []
        self.config = config
        commit_line = string.split("|")

        if commit_line.__len__() == 5:
            self.timestamp = commit_line[0]
            self.date = commit_line[1]
            self.sha = commit_line[2]
            author = commit_line[3].strip()
            email = commit_line[4].strip()
            (self.author, self.email) = Commit.get_alias(author, email, self.config)

    def __lt__(self, other):
        return self.timestamp.__lt__(other.timestamp) # only used for sorting; we just consider the timestamp.

    def add_filediff(self, filediff):
        self.filediffs.append(filediff)

    def get_filediffs(self):
        return self.filediffs

    @staticmethod
    def get_alias(author, email, config):
        author_mail = "{0} <{1}>".format(author, email)
        if author_mail in config.aliases.keys():
            new_author_mail = config.aliases[author_mail].split("<")
            return (new_author_mail[0].strip(), new_author_mail[1][0:-1])

        return (author, email)

    @staticmethod
    def get_author_and_email(config, changes, string):
        commit_line = string.split("|")
        try:
            author = commit_line[3].strip()
            email = commit_line[4].strip()
            (real_author, real_email) = Commit.get_alias(author, email, config)
            changes.emails_by_author[author] = real_email
            changes.authors_by_email[email]  = real_author
            if changes.colors_by_author.get(real_author) is None:
                changes.colors_by_author[real_author] = AuthorColors.get_new_color()
            changes.colors_by_author[author] = changes.colors_by_author[real_author]
            return (real_author, real_email)
        except IndexError:
            return "Unknown Author"

    @staticmethod
    def is_commit_line(string):
        return string.split("|").__len__() == 5


class AuthorInfo(object):
    email = None
    insertions = 0
    deletions = 0
    commits = 0


class ChangesThread(threading.Thread):
    def __init__(self, config, changes, first_hash, second_hash, offset):
        __thread_lock__.acquire() # Lock controlling the number of threads running
        threading.Thread.__init__(self)

        self.config = config
        self.changes = changes
        self.first_hash = first_hash
        self.second_hash = second_hash
        self.offset = offset

    @staticmethod
    def create(config, changes, first_hash, second_hash, offset):
        thread = ChangesThread(config, changes, first_hash, second_hash, offset)
        thread.daemon = True
        thread.start()

    def run(self):
        git_log_r = subprocess.Popen(filter(None,
                                            ["git", "log", "--reverse", "--pretty=%ct|%cd|%H|%aN|%aE",
                                             "--stat=100000,8192", "--no-merges", "-w", interval.get_since(),
                                             interval.get_until(),
                                             "--date=short"] + (["-C", "-C", "-M"] if self.config.hard else []) +
                                            [self.first_hash + self.second_hash]), bufsize=1, stdout=subprocess.PIPE)
        lines = git_log_r.stdout.readlines()
        git_log_r.wait()
        git_log_r.stdout.close()

        commit = None
        found_valid_extension = False
        has_been_filtered = False
        commits = []

        __changes_lock__.acquire() # Global lock used to protect calls from here...

        for i in lines:
            j = i.strip().decode("unicode_escape", "ignore")
            j = j.encode("latin-1", "replace")
            j = j.decode("utf-8", "replace")

            if Commit.is_commit_line(j):
                (author, email) = Commit.get_author_and_email(self.config, self.changes, j)

            if Commit.is_commit_line(j) or i is lines[-1]:
                if found_valid_extension:
                    bisect.insort(commits, commit)

                found_valid_extension = False
                has_been_filtered = False
                commit = Commit(j, self.config)

                if Commit.is_commit_line(j) and \
                   (is_filtered(commit.author, Filters.AUTHOR) or \
                    is_filtered(commit.email,  Filters.EMAIL) or \
                    is_filtered(commit.sha,    Filters.REVISION) or \
                    is_filtered(commit.sha,    Filters.MESSAGE)):
                    has_been_filtered = True

            if FileDiff.is_filediff_line(j) and not has_been_filtered:
                if FileDiff.is_valid_extension(j):
                    found_valid_extension = True
                    filediff = FileDiff(j)
                    commit.add_filediff(filediff)

        self.changes.commits[self.offset // CHANGES_PER_THREAD] = commits
        __changes_lock__.release() # ...to here.
        __thread_lock__.release() # Lock controlling the number of threads running


PROGRESS_TEXT = _("Fetching and calculating primary statistics (1 of 2): {0:.0f}%")


class Changes(object):

    @classmethod
    def empty(cls):
        changes = Changes.__new__(Changes)
        changes.commits = []
        changes.authors = {}
        changes.authors_dateinfo = {}
        changes.authors_by_email = {}
        changes.emails_by_author = {}
        changes.colors_by_author = {}
        return changes

    def __init__(self, repo, config):
        self.commits = []
        self.authors = {}
        self.authors_dateinfo = {}
        self.authors_by_email = {}
        self.emails_by_author = {}
        self.colors_by_author = {}
        self.config = config

        interval.set_ref("HEAD")
        git_rev_list_p = subprocess.Popen(filter(None, ["git", "rev-list", "--reverse", "--no-merges",
                                                        interval.get_since(), interval.get_until(), "HEAD"]),
                                          bufsize=1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        lines = git_rev_list_p.communicate()[0].splitlines()
        git_rev_list_p.wait()
        git_rev_list_p.stdout.close()

        if git_rev_list_p.returncode == 0 and lines:
            progress_text = _(PROGRESS_TEXT)
            if repo is not None:
                progress_text = "[%s] " % repo.name + progress_text

            chunks = len(lines) // CHANGES_PER_THREAD
            self.commits = [None] * (chunks if len(lines) % CHANGES_PER_THREAD == 0 else chunks + 1)
            first_hash = ""

            for i, entry in enumerate(lines):
                if i % CHANGES_PER_THREAD == CHANGES_PER_THREAD - 1:
                    entry = entry.decode("utf-8", "replace").strip()
                    second_hash = entry
                    ChangesThread.create(self.config, self, first_hash, second_hash, i)
                    first_hash = entry + ".."

                    if self.config.progress and format.is_interactive_format():
                        terminal.output_progress(progress_text, i, len(lines))
            else:
                if CHANGES_PER_THREAD - 1 != i % CHANGES_PER_THREAD:
                    entry = entry.decode("utf-8", "replace").strip()
                    second_hash = entry
                    ChangesThread.create(self.config, self, first_hash, second_hash, i)

        # Make sure all threads have completed.
        for i in range(0, NUM_THREADS):
            __thread_lock__.acquire()

        # We also have to release them for future use.
        for i in range(0, NUM_THREADS):
            __thread_lock__.release()

        self.commits = [item for sublist in self.commits for item in sublist]

        if self.commits:
            if interval.has_interval():
                interval.set_ref(self.commits[-1].sha)

            self.first_commit_date = datetime.date(int(self.commits[0].date[0:4]),
                                                   int(self.commits[0].date[5:7]),
                                                   int(self.commits[0].date[8:10]))
            self.last_commit_date = datetime.date(int(self.commits[-1].date[0:4]),
                                                  int(self.commits[-1].date[5:7]),
                                                  int(self.commits[-1].date[8:10]))

    def __iadd__(self, other):
        try:
            self.authors.update(other.authors)
            self.authors_dateinfo.update(other.authors_dateinfo)
            self.authors_by_email.update(other.authors_by_email)
            self.emails_by_author.update(other.emails_by_author)
            self.colors_by_author.update(other.colors_by_author)

            for commit in other.commits:
                bisect.insort(self.commits, commit)
            if not self.commits and not other.commits:
                self.commits = []

            return self
        except AttributeError:
            return other

    def get_commits(self):
        return self.commits

    def update_dict_commit(self, dict, key, commit):
        if dict.get(key, None) is None:
            dict[key] = AuthorInfo()

        if commit.get_filediffs():
            dict[key].commits += 1

        for j in commit.get_filediffs():
            dict[key].insertions += j.insertions
            dict[key].deletions += j.deletions

    def get_authorinfo_list(self):
        if not self.authors:
            for i in self.commits:
                self.update_dict_commit(self.authors, i.author, i)

        return copy.deepcopy(self.authors)

    def get_authordateinfo_list(self):
        if not self.authors_dateinfo:
            for i in self.commits:
                self.update_dict_commit(self.authors_dateinfo, (i.date, i.author), i)

        return copy.deepcopy(self.authors_dateinfo)

    def get_latest_author_by_email(self, email):
        if not hasattr(email, "decode"):
            email = str.encode(email)
        try:
            email = email.decode("unicode_escape", "ignore")
        except UnicodeEncodeError:
            pass

        return self.authors_by_email[email]

    def get_latest_email_by_author(self, name):
        return self.emails_by_author[name]
