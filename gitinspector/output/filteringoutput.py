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

import os
import string
import textwrap

from ..changes import FileType
from ..filtering import get_filtered, has_filtered, Filters
from .outputable import Outputable
from .. import terminal

FILTERING_FILE_INFO_TEXT = lambda: _("The following files were excluded from the statistics due to the specified exclusion patterns")
FILTERING_AUTHOR_INFO_TEXT = lambda: _("The following authors were excluded from the statistics due to the specified exclusion patterns")
FILTERING_EMAIL_INFO_TEXT = lambda: _("The authors with the following emails were excluded from the statistics due to the specified " \
                              "exclusion patterns")
FILTERING_COMMIT_INFO_TEXT = lambda: _("The following commit revisions were excluded from the statistics due to the specified " \
                               "exclusion patterns")

class FilteringOutput(Outputable):
    output_order = 600

    def __init__(self, runner):
        Outputable.__init__(self)
        self.display = bool(runner.changes.all_commits())
        self.changes = runner.changes
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
        authorinfo_dict = self.changes.get_authorinfo_list()
        filtered_files = {k:self.changes.filtered_files(k) for k in authorinfo_dict}
        filtered_sizes = [len(s) for s in filtered_files.values()]
        if has_filtered() or any(filtered_sizes):
            other_files = "<table class='git2'>"
            par = "even"
            for committer, files in filtered_files.items():
                if (len(files)>0):
                    if len(files) > 20:
                        old_len = len(files)
                        files = list(files)[0:20] + ["... and {0} other files".format(old_len-20)]
                    par   = "even" if par == "odd" else "odd"
                    color = self.changes.committers[committer]["color"]
                    rect  = ("<svg width='16' height='16'><rect x='5' y='5' "
                             "width='16' height='16' fill='{0}'></rect></svg>").\
                             format(color)
                    other_files += "<tr class='{0}'><td style='text-align:left'>{1} {2}</td><td>{3}</td></tr>".\
                        format(par, rect, committer[0], ", ".join(files))
            other_files += "</table>"

            temp_file = os.path.join(os.path.dirname(__file__),
                                     "../templates/filtering_output.html")
            with open(temp_file, 'r') as infile:
                src = string.Template( infile.read() )
                self.out.write(src.substitute(
                    other_files=other_files,
                    files_filtering_text=FILTERING_FILE_INFO_TEXT(),
                    files_filtered=", ".join(get_filtered(Filters.FILE_OUT)),
                    authors_filtering_text=FILTERING_AUTHOR_INFO_TEXT(),
                    authors_filtered=", ".join(get_filtered(Filters.AUTHOR)),
                    emails_filtering_text=FILTERING_EMAIL_INFO_TEXT(),
                    emails_filtered=", ".join(get_filtered(Filters.EMAIL)),
                    commits_filtering_text=FILTERING_COMMIT_INFO_TEXT(),
                    commits_filtered=", ".join(get_filtered(Filters.REVISION)),
                ))

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
            output += FilteringOutput.__output_json_section__(FILTERING_FILE_INFO_TEXT(),
                                                              get_filtered(Filters.FILE_OUT), "files")
            output += FilteringOutput.__output_json_section__(FILTERING_AUTHOR_INFO_TEXT(),
                                                              get_filtered(Filters.AUTHOR), "authors")
            output += FilteringOutput.__output_json_section__(FILTERING_EMAIL_INFO_TEXT(),
                                                              get_filtered(Filters.EMAIL), "emails")
            output += FilteringOutput.__output_json_section__(FILTERING_COMMIT_INFO_TEXT(),
                                                              get_filtered(Filters.REVISION), "revision")
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
        self.__output_text_section__(FILTERING_FILE_INFO_TEXT(), get_filtered(Filters.FILE_OUT))
        self.__output_text_section__(FILTERING_AUTHOR_INFO_TEXT(), get_filtered(Filters.AUTHOR))
        self.__output_text_section__(FILTERING_EMAIL_INFO_TEXT(), get_filtered(Filters.EMAIL))
        self.__output_text_section__(FILTERING_COMMIT_INFO_TEXT(), get_filtered(Filters.REVISION))

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
            self.__output_xml_section__(FILTERING_FILE_INFO_TEXT(),
                                        get_filtered(Filters.FILE_OUT), "files")
            self.__output_xml_section__(FILTERING_AUTHOR_INFO_TEXT(),
                                        get_filtered(Filters.AUTHOR), "authors")
            self.__output_xml_section__(FILTERING_EMAIL_INFO_TEXT(),
                                        get_filtered(Filters.EMAIL), "emails")
            self.__output_xml_section__(FILTERING_COMMIT_INFO_TEXT(),
                                        get_filtered(Filters.REVISION), "revision")
            self.out.writeln("\t</filtering>")
