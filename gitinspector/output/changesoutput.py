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

import json
import textwrap
from .. import format, gravatar, terminal
from .outputable import Outputable

HISTORICAL_INFO_TEXT = _("The following historical commit information, by author, was found in the repository")
NO_COMMITED_FILES_TEXT = _("No commited files with the specified extensions were found")


class ChangesOutput(Outputable):
    output_order = 100

    def __init__(self, runner):
        Outputable.__init__(self)
        self.changes = runner.changes
        self.display = True
        self.out = runner.out

    def output_html(self):
        authorinfo_list = self.changes.get_authorinfo_list()
        total_changes = 0.0
        changes_xml = "<div><div class=\"box\">"
        chart_data = ""

        for i in authorinfo_list:
            total_changes += authorinfo_list.get(i).insertions
            total_changes += authorinfo_list.get(i).deletions

        if authorinfo_list:
            changes_xml += "<p>" + _(HISTORICAL_INFO_TEXT) + ".</p><div><table id=\"changes\" class=\"git\">"
            changes_xml += "<thead><tr><th>{0}</th> <th>{1}</th> <th>{2}</th> <th>{3}</th> <th>{4}</th>".format(_("Author"),
                                                                                                                _("Commits"),
                                                                                                                _("Insertions"),
                                                                                                                _("Deletions"),
                                                                                                                _("% of changes"))
            changes_xml += "</tr></thead><tbody>"

            for i, entry in enumerate(sorted(authorinfo_list)):
                authorinfo = authorinfo_list.get(entry)
                percentage = 0 if total_changes == 0 else (authorinfo.insertions + authorinfo.deletions) / total_changes * 100

                changes_xml += "<tr " + ("class=\"odd\">" if i % 2 == 1 else ">")

                if format.get_selected() == "html":
                    changes_xml += "<td>"
                    changes_xml += "<img src=\"{0}\"/>".format(gravatar.get_url(self.changes.get_latest_email_by_author(entry)))
                    changes_xml += "{0}</td>".format(entry)
                else:
                    changes_xml += "<td>" + entry + "</td>"

                changes_xml += "<td>" + str(authorinfo.commits) + "</td>"
                changes_xml += "<td>" + str(authorinfo.insertions) + "</td>"
                changes_xml += "<td>" + str(authorinfo.deletions) + "</td>"
                changes_xml += "<td>" + "{0:.2f}".format(percentage) + "</td>"
                changes_xml += "</tr>"
                chart_data += "{{label: {0}, data: {1}}}".format(json.dumps(entry), "{0:.2f}".format(percentage))

                if sorted(authorinfo_list)[-1] != entry:
                    chart_data += ", "

            changes_xml += ("<tfoot><tr> <td colspan=\"5\">&nbsp;</td> </tr></tfoot></tbody></table>")
            changes_xml += "<div class=\"chart\" id=\"changes_chart\"></div></div>"
            changes_xml += "<script type=\"text/javascript\">"
            changes_xml += "    changes_plot = $.plot($(\"#changes_chart\"), [{0}], {{".format(chart_data)
            changes_xml += "    series: {"
            changes_xml += "        pie: {"
            changes_xml += "        innerRadius: 0.4,"
            changes_xml += "        show: true,"
            changes_xml += "        combine: {"
            changes_xml += "            threshold: 0.01,"
            changes_xml += "            label: \"" + _("Minor Authors") + "\""
            changes_xml += "        }"
            changes_xml += "        }"
            changes_xml += "    }, grid: {"
            changes_xml += "        hoverable: true"
            changes_xml += "    }"
            changes_xml += "    });"
            changes_xml += "</script>"
        else:
            changes_xml += "<p>" + _(NO_COMMITED_FILES_TEXT) + ".</p>"

        changes_xml += "</div></div>"
        self.out.writeln(changes_xml)

    def output_json(self):
        authorinfo_list = self.changes.get_authorinfo_list()
        total_changes = 0.0

        for i in authorinfo_list:
            total_changes += authorinfo_list.get(i).insertions
            total_changes += authorinfo_list.get(i).deletions

        if authorinfo_list:
            message_json = "\t\t\t\"message\": \"" + _(HISTORICAL_INFO_TEXT) + "\",\n"
            changes_json = ""

            for i in sorted(authorinfo_list):
                author_email = self.changes.get_latest_email_by_author(i)
                authorinfo = authorinfo_list.get(i)
                percentage = 0 if total_changes == 0 else (authorinfo.insertions + authorinfo.deletions) / total_changes * 100

                changes_json += "{\n"
                changes_json += "\t\t\t\t\"name\": \"" + i + "\",\n"
                changes_json += "\t\t\t\t\"email\": \"" + author_email + "\",\n"
                changes_json += "\t\t\t\t\"gravatar\": \"" + gravatar.get_url(author_email) + "\",\n"
                changes_json += "\t\t\t\t\"commits\": " + str(authorinfo.commits) + ",\n"
                changes_json += "\t\t\t\t\"insertions\": " + str(authorinfo.insertions) + ",\n"
                changes_json += "\t\t\t\t\"deletions\": " + str(authorinfo.deletions) + ",\n"
                changes_json += "\t\t\t\t\"percentage_of_changes\": " + "{0:.2f}".format(percentage) + "\n"
                changes_json += "\t\t\t},"

            # Removing the last trailing ','
            changes_json = changes_json[:-1]

            self.out.write("\t\t\"changes\": {\n" + message_json + "\t\t\t\"authors\": [\n\t\t\t" + changes_json + "]\n\t\t}")
        else:
            self.out.writeln("\t\t\"exception\": \"" + _(NO_COMMITED_FILES_TEXT) + "\"")

    def output_text(self):
        authorinfo_list = self.changes.get_authorinfo_list()
        total_changes = 0.0

        for i in authorinfo_list:
            total_changes += authorinfo_list.get(i).insertions
            total_changes += authorinfo_list.get(i).deletions

        if authorinfo_list:
            self.out.writeln(textwrap.fill(_(HISTORICAL_INFO_TEXT) + ":", width=terminal.get_size()[0]))
            self.out.writeln("")
            terminal.writeb(self.out,
                            terminal.ljust(_("Author"), 21) + terminal.rjust(_("Commits"), 13) +
                            terminal.rjust(_("Insertions"), 14) + terminal.rjust(_("Deletions"), 15) +
                            terminal.rjust(_("% of changes"), 16) + "\n")

            for i in sorted(authorinfo_list):
                authorinfo = authorinfo_list.get(i)
                percentage = 0 if total_changes == 0 else \
                             (authorinfo.insertions + authorinfo.deletions) / total_changes * 100

                self.out.write(terminal.ljust(i, 20)[0:20 - terminal.get_excess_column_count(i)])
                self.out.write(str(authorinfo.commits).rjust(14))
                self.out.write(str(authorinfo.insertions).rjust(14))
                self.out.write(str(authorinfo.deletions).rjust(15))
                self.out.writeln("{0:.2f}".format(percentage).rjust(16))
        else:
            self.out.writeln(_(NO_COMMITED_FILES_TEXT) + ".")
        self.out.writeln("")

    def output_xml(self):
        authorinfo_list = self.changes.get_authorinfo_list()
        total_changes = 0.0

        for i in authorinfo_list:
            total_changes += authorinfo_list.get(i).insertions
            total_changes += authorinfo_list.get(i).deletions

        if authorinfo_list:
            message_xml = "\t\t<message>" + _(HISTORICAL_INFO_TEXT) + "</message>\n"
            changes_xml = ""

            for i in sorted(authorinfo_list):
                author_email = self.changes.get_latest_email_by_author(i)
                authorinfo = authorinfo_list.get(i)
                percentage = 0 if total_changes == 0 else (authorinfo.insertions + authorinfo.deletions) / total_changes * 100

                changes_xml += "\t\t\t<author>\n"
                changes_xml += "\t\t\t\t<name>" + i + "</name>\n"
                changes_xml += "\t\t\t\t<email>" + author_email + "</email>\n"
                changes_xml += "\t\t\t\t<gravatar>" + gravatar.get_url(author_email) + "</gravatar>\n"
                changes_xml += "\t\t\t\t<commits>" + str(authorinfo.commits) + "</commits>\n"
                changes_xml += "\t\t\t\t<insertions>" + str(authorinfo.insertions) + "</insertions>\n"
                changes_xml += "\t\t\t\t<deletions>" + str(authorinfo.deletions) + "</deletions>\n"
                changes_xml += "\t\t\t\t<percentage-of-changes>" + "{0:.2f}".format(percentage) + \
                               "</percentage-of-changes>\n"
                changes_xml += "\t\t\t</author>\n"

            self.out.writeln("\t<changes>\n" + message_xml + "\t\t<authors>\n" +
                             changes_xml + "\t\t</authors>\n\t</changes>")
        else:
            self.out.writeln("\t<changes>\n\t\t<exception>" + _(NO_COMMITED_FILES_TEXT) +
                             "</exception>\n\t</changes>")
