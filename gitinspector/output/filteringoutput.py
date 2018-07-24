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

import textwrap
from ..filtering import __filters__, has_filtered
from .. import terminal
from .outputable import Outputable

FILTERING_INFO_TEXT = _("The following files were excluded from the statistics due to the specified exclusion patterns")
FILTERING_AUTHOR_INFO_TEXT = _("The following authors were excluded from the statistics due to the specified exclusion patterns")
FILTERING_EMAIL_INFO_TEXT = _("The authors with the following emails were excluded from the statistics due to the specified " \
                              "exclusion patterns")
FILTERING_COMMIT_INFO_TEXT = _("The following commit revisions were excluded from the statistics due to the specified " \
                               "exclusion patterns")

class FilteringOutput(Outputable):
    output_order = 600

    def __init__(self, runner):
        Outputable.__init__(self)
        self.display = bool(runner.changes.commits)
        self.out = runner.out

    @staticmethod
    def __output_html_section__(info_string, filtered):
        filtering_xml = ""

        if filtered:
            filtering_xml += "<p>" + info_string + "."+ "</p>"

            for i in filtered:
                filtering_xml += "<p>" + i + "</p>"

        return filtering_xml

    def output_html(self):
        if has_filtered():
            filtering_xml = "<div><div class=\"box\">"
            FilteringOutput.__output_html_section__(_(FILTERING_INFO_TEXT), __filters__["file"][1])
            FilteringOutput.__output_html_section__(_(FILTERING_AUTHOR_INFO_TEXT), __filters__["author"][1])
            FilteringOutput.__output_html_section__(_(FILTERING_EMAIL_INFO_TEXT), __filters__["email"][1])
            FilteringOutput.__output_html_section__(_(FILTERING_COMMIT_INFO_TEXT), __filters__["revision"][1])
            filtering_xml += "</div></div>"

            self.out.writeln(filtering_xml)

    @staticmethod
    def __output_json_section__(info_string, filtered, container_tagname):
        if filtered:
            message_json = "\t\t\t\t\"message\": \"" + info_string + "\",\n"
            filtering_json = ""

            for i in filtered:
                filtering_json += "\t\t\t\t\t\"" + i + "\",\n"
            # Removing the last trailing '\n'
            filtering_json = filtering_json[:-3]

            return "\n\t\t\t\"{0}\": {{\n".format(container_tagname) + message_json + \
                "\t\t\t\t\"entries\": [\n" + filtering_json + "\"\n\t\t\t\t]\n\t\t\t},"

        return ""

    def output_json(self):
        if has_filtered():
            output = ",\n\t\t\"filtering\": {"
            output += FilteringOutput.__output_json_section__(_(FILTERING_INFO_TEXT),
                                                              __filters__["file"][1], "files")
            output += FilteringOutput.__output_json_section__(_(FILTERING_AUTHOR_INFO_TEXT),
                                                              __filters__["author"][1], "authors")
            output += FilteringOutput.__output_json_section__(_(FILTERING_EMAIL_INFO_TEXT),
                                                              __filters__["email"][1], "emails")
            output += FilteringOutput.__output_json_section__(_(FILTERING_COMMIT_INFO_TEXT),
                                                              __filters__["revision"][1], "revision")
            output = output[:-1]
            output += "\n\t\t}"
            self.out.write(output)

    def __output_text_section__(self, info_string, filtered):
        if filtered:
            self.out.writeln("\n" + textwrap.fill(info_string + ":", width=terminal.get_size()[0]))

            for i in filtered:
                (width, _unused) = terminal.get_size()
                self.out.writeln("...%s" % i[-width+3:] if len(i) > width else i)

    def output_text(self):
        self.__output_text_section__(_(FILTERING_INFO_TEXT), __filters__["file"][1])
        self.__output_text_section__(_(FILTERING_AUTHOR_INFO_TEXT), __filters__["author"][1])
        self.__output_text_section__(_(FILTERING_EMAIL_INFO_TEXT), __filters__["email"][1])
        self.__output_text_section__(_(FILTERING_COMMIT_INFO_TEXT), __filters__["revision"][1])

    def __output_xml_section__(self, info_string, filtered, container_tagname):
        if filtered:
            message_xml = "\t\t\t<message>" + info_string + "</message>\n"
            filtering_xml = ""

            for i in filtered:
                filtering_xml += "\t\t\t\t<entry>" + i + "</entry>\n"

            self.out.writeln("\t\t<{0}>".format(container_tagname))
            self.out.writeln(message_xml + "\t\t\t<entries>\n" + filtering_xml + "\t\t\t</entries>\n")
            self.out.writeln("\t\t</{0}>".format(container_tagname))

    def output_xml(self):
        if has_filtered():
            self.out.writeln("\t<filtering>")
            self.__output_xml_section__(_(FILTERING_INFO_TEXT), __filters__["file"][1], "files")
            self.__output_xml_section__(_(FILTERING_AUTHOR_INFO_TEXT), __filters__["author"][1], "authors")
            self.__output_xml_section__(_(FILTERING_EMAIL_INFO_TEXT), __filters__["email"][1], "emails")
            self.__output_xml_section__(_(FILTERING_COMMIT_INFO_TEXT), __filters__["revision"][1], "revision")
            self.out.writeln("\t</filtering>")
