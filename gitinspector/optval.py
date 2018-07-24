# coding: utf-8
#
# Copyright © 2013 Ejwa Software. All rights reserved.
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


class InvalidOptionArgument(Exception):
    def __init__(self, msg):
        super(InvalidOptionArgument, self).__init__(msg)
        self.msg = msg


def get_boolean_argument(arg):
    if isinstance(arg, bool):
        return arg
    elif arg is None or arg.lower() == "false" or arg.lower() == "f" or arg == "0":
        return False
    elif arg.lower() == "true" or arg.lower() == "t" or arg == "1":
        return True

    raise InvalidOptionArgument(_("The given option argument is not a valid boolean."))
