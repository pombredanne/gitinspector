# coding: utf-8
#
# Copyright © 2012-2015 Ejwa Software. All rights reserved.
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

import re
import subprocess

__filters__ = {
    "file": [set(), set()],
    "author": [set(), set()],
    "email": [set(), set()],
    "revision": [set(), set()],
    "message" : [set(), None]
}

class InvalidRegExpError(ValueError):
    def __init__(self, msg):
        super(InvalidRegExpError, self).__init__(msg)
        self.msg = msg

# -- Unused function
# def get():
#     return __filters__

def __add_one_filter__(string):
    """
    Function that takes a string of the form 'KEY:PAT' and adds the
    records the corresponding filter inside __filters__. The syntax
    corresponds to the --exclude option on the command-line. If KEY is
    missing somehow, the filter is automatically "file".
    """
    for i in __filters__:
        if (i + ":").lower() == string[0:len(i) + 1].lower():
            __filters__[i][0].add(string[len(i) + 1:])
            return
    __filters__["file"][0].add(string)

def add(string):
    """
    Add a set of filters, separated by commas.
    """
    rules = string.split(",")
    for rule in rules:
        __add_one_filter__(rule)

def clear():
    for i in __filters__:
        __filters__[i] = [set(), set()]

def get_filtered(filter_type="file"):
    return __filters__[filter_type][1]

# Returns True iff there is at least one active filter
def has_filtered():
    for i in __filters__:
        if __filters__[i][1]:
            return True
    return False

def __find_commit_message__(sha):
    git_show_r = subprocess.Popen(filter(None, ["git", "show", "-s",
                                                "--pretty=%B", "-w", sha]), bufsize=1,
                                  stdout=subprocess.PIPE)
    commit_message = git_show_r.stdout.read()
    git_show_r.wait()
    git_show_r.stdout.close()

    commit_message = commit_message.strip().decode("unicode_escape", "ignore")
    commit_message = commit_message.encode("latin-1", "replace")
    return commit_message.decode("utf-8", "replace")

def set_filtered(string, filter_type="file"):
    """
    The function that filters the commits according to the filters
    defined in __filters__. The string parameter depends on the filter_type.
    """
    string = string.strip()
    if not string:
        return False

    for i in __filters__[filter_type][0]:
        if filter_type == "message":
            search_for = __find_commit_message__(string)
        else:
            search_for = string

        try:
            if re.search(i, search_for) is not None:
                if filter_type == "message":
                    __add_one_filter__("revision:" + string) # ??
                else:
                    __filters__[filter_type][1].add(string)
                return True
        except:
            raise InvalidRegExpError(_("Invalid regular expression specified"))

    return False
