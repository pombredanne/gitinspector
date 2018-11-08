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

DEFAULT_EXTENSIONS = ["java", "c", "cc", "cpp", "h", "hh", "hpp", "py", "glsl", "rb", "js", "sql"]

__extensions__ = DEFAULT_EXTENSIONS
__located_extensions__ = set()

def get():
    return __extensions__

def define(string):
    global __extensions__
    __extensions__ = string.split(",")

def add_located(string):
    if string:
        __located_extensions__.add(string)
    else:
        __located_extensions__.add("*")

def get_located():
    return __located_extensions__

# The semantics of this file is the following: it contains two sets of
# strings.
#
# - the first set of strings is named __extensions__, can be
#   configured via the command line, and specifies a set of extensions
#   that will be considered through the analysis
#
# - the second set is named __located_extensions__, and lists the
#   extensions that have been found during the analysis. Recall that
#   with the "-x" flag, some commits can be excluded from analysis, so
#   not all files in the repository will be found, even if all
#   extensions are allowed
