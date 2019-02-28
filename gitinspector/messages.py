# coding: utf-8
#
# Copyright © 2019 Emmanuel Fleury. All rights reserved.
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

import sys

EXEC_NAME = "gitinspector"

def error(msg):
    """Display an error message and quit the program with a failure code."""
    sys.stderr.write(EXEC_NAME + ": error: " + msg + "\n")
    sys.stderr.write("Try `" + EXEC_NAME + " --help' for more information.\n")
    sys.exit(1)

def warning(msg):
    """Display a warning message and keep going on the """
    sys.stderr.write(EXEC_NAME + ": warning: " + msg + "\n")

def debug(msg):
    sys.stderr.write(EXEC_NAME + ": debug: " + msg + "\n")
