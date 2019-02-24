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
import os
import string
import textwrap
from .. import format, gravatar, terminal
from .outputable import Outputable

HISTORICAL_INFO_TEXT = lambda: _("The following historical commit information, by author, was found in the repository")
NO_COMMITED_FILES_TEXT = lambda: _("No commited files with the specified extensions were found")


class ChangesOutput(Outputable):
    output_order = 100

    def __init__(self, runner):
        Outputable.__init__(self)
        self.changes = runner.changes
        self.display = True
        self.out = runner.out

    def output_html(self):
        authorinfo_dict = self.changes.get_authorinfo_list()
        author_list = list(authorinfo_dict.keys())
        author_list.sort(key=lambda x: authorinfo_dict[x].insertions + \
                         authorinfo_dict[x].deletions, reverse=True)
        data_array = []

        # Compute total changes
        total_changes = 0.0
        for i in authorinfo_dict:
            total_changes += authorinfo_dict.get(i).insertions
            total_changes += authorinfo_dict.get(i).deletions

        for committer in author_list:
            authorinfo = authorinfo_dict.get(committer)
            percentage = 0 if total_changes == 0 else \
                (authorinfo.insertions + authorinfo.deletions) / total_changes * 100

            data_array.append({
                "avatar": "<img src=\"{0}\"/>".format(gravatar.get_url(committer[1])),
                "color": self.changes.committers[committer]["color"],
                "name":  committer[0],
                "commits" : authorinfo.commits,
                "insertions" : authorinfo.insertions,
                "deletions" : authorinfo.deletions,
                "changes" : round(percentage,2),
                })

        temp_file = os.path.join(os.path.dirname(__file__),
                                 "../templates/changes_output.html")
        with open(temp_file, 'r') as infile:
            src = string.Template( infile.read() )
            self.out.write(src.substitute(
                changes_data=str(data_array),
            ))

    def output_json(self):
        authorinfo_list = self.changes.get_authorinfo_list()
        total_changes = 0.0

        for i in authorinfo_list:
            total_changes += authorinfo_list.get(i).insertions
            total_changes += authorinfo_list.get(i).deletions

        if authorinfo_list:
            message_json = "\t\t\t\"message\": \"" + HISTORICAL_INFO_TEXT() + "\",\n"
            changes_json = ""

            for committer in sorted(authorinfo_list):
                (author_name, author_email) = committer
                authorinfo = authorinfo_list.get(committer)
                percentage = 0 if total_changes == 0 else \
                    (authorinfo.insertions + authorinfo.deletions) / total_changes * 100

                changes_json += "{\n"
                changes_json += "\t\t\t\t\"name\": \"" + author_name + "\",\n"
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
            self.out.writeln("\t\t\"exception\": \"" + NO_COMMITED_FILES_TEXT() + "\"")

    def output_text(self):
        authorinfo_list = self.changes.get_authorinfo_list()
        total_changes = 0.0

        for i in authorinfo_list:
            total_changes += authorinfo_list.get(i).insertions
            total_changes += authorinfo_list.get(i).deletions

        if authorinfo_list:
            self.out.writeln(textwrap.fill(HISTORICAL_INFO_TEXT() + ":", width=terminal.get_size()[0]))
            self.out.writeln("")
            terminal.writeb(self.out,
                            terminal.ljust(_("Author"), 21) + terminal.rjust(_("Commits"), 13) +
                            terminal.rjust(_("Insertions"), 14) + terminal.rjust(_("Deletions"), 15) +
                            terminal.rjust(_("% of changes"), 16) + "\n")

            for i in sorted(authorinfo_list):
                authorinfo = authorinfo_list.get(i)
                percentage = 0 if total_changes == 0 else \
                             (authorinfo.insertions + authorinfo.deletions) / total_changes * 100

                self.out.write(terminal.ljust(i[0], 20)[0:20 - terminal.get_excess_column_count(i[0])])
                self.out.write(str(authorinfo.commits).rjust(14))
                self.out.write(str(authorinfo.insertions).rjust(14))
                self.out.write(str(authorinfo.deletions).rjust(15))
                self.out.writeln("{0:.2f}".format(percentage).rjust(16))
        else:
            self.out.writeln(NO_COMMITED_FILES_TEXT() + ".")
        self.out.writeln("")

    def output_xml(self):
        authorinfo_list = self.changes.get_authorinfo_list()
        total_changes = 0.0

        for i in authorinfo_list:
            total_changes += authorinfo_list.get(i).insertions
            total_changes += authorinfo_list.get(i).deletions

        if authorinfo_list:
            message_xml = "\t\t<message>" + HISTORICAL_INFO_TEXT() + "</message>\n"
            changes_xml = ""

            for committer in sorted(authorinfo_list):
                (author_name, author_email) = committer
                authorinfo = authorinfo_list.get(committer)
                percentage = 0 if total_changes == 0 else (authorinfo.insertions + authorinfo.deletions) / total_changes * 100

                changes_xml += "\t\t\t<author>\n"
                changes_xml += "\t\t\t\t<name>" + author_name + "</name>\n"
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
            self.out.writeln("\t<changes>\n\t\t<exception>" + NO_COMMITED_FILES_TEXT() +
                             "</exception>\n\t</changes>")
