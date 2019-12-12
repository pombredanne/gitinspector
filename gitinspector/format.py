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

import base64
import os
import sys
import textwrap
import time

from . import basedir, localization, terminal, version

__available_formats__ = ["html", "htmlembedded", "json", "text", "xml"]

DEFAULT_FORMAT = __available_formats__[3]

__selected_format__ = DEFAULT_FORMAT

class InvalidFormatError(Exception):
    def __init__(self, msg):
        super(InvalidFormatError, self).__init__(msg)
        self.msg = msg

def select(format):
    global __selected_format__
    __selected_format__ = format

    return format in __available_formats__

def get_selected():
    return __selected_format__

def is_interactive_format():
    return __selected_format__ == "text"

def __output_html_template__(name):
    template_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), name)
    file_r = open(template_path, "rb")
    template = file_r.read().decode("utf-8", "replace")

    file_r.close()
    return template

INFO_START_ONE_REPO   = lambda: _("Statistical information for the repository")
INFO_START_MANY_REPOS = lambda: _("Statistical information for the repositories")
INFO_MID_ANY_REPO     = lambda: _("was gathered on the")

def output_header(runner):
    """
    The function responsible for outputting a header to the
    output. For the HTML-like outputs, this also means handling the
    different Javascript files that are included or not inside the
    output.
    """
    repos = runner.repos
    repos_string = ", ".join([repo.name for repo in repos])

    if __selected_format__ == "html" or __selected_format__ == "htmlembedded":
        base = basedir.get_basedir()
        html_header = __output_html_template__(base + "/templates/header.html")

        logo_file = open(base + "/html/gitinspector_piclet.png", "rb")
        logo = logo_file.read()
        logo_file.close()
        logo = base64.b64encode(logo)

        if __selected_format__ == "htmlembedded":
            jquery_js = "<script type='application/javascript'>" + \
                __output_html_template__(base + "/html/jquery.min.js") + "</script>"
            d3_js = "<script type='application/javascript'>" + \
                __output_html_template__(base + "/html/d3.min.js") + "</script>"
        else:
            jquery_js = ("<script type='application/javascript' "
                         "src='https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js'>"
                         "</script>")
            d3_js = ("<script type='application/javascript' "
                     "src='https://ajax.googleapis.com/ajax/libs/d3js/5.7.0/d3.min.js'>"
                     "</script>")

        custom_js = "<script type='application/javascript'>" + \
            __output_html_template__(base + "/html/custom.js") + "</script>"
        style_css = "<style type='text/css'>" + \
            __output_html_template__(base + "/html/style.css") + "</style>"

        repos_name = (repos_string if runner.config.branch == "--all"
                     else "%s (branch %s)"%(repos_string, runner.config.branch))
        repos_text = (INFO_START_ONE_REPO() if len(repos) <= 1 else
                      INFO_START_MANY_REPOS()) + \
                      " <span class='repo_title'>{0}</span> ".format(repos_name) + \
                      INFO_MID_ANY_REPO() + \
                      " <span class='repo_title'>{0}</span>.".format(localization.get_date())

        logo_text = _("The output has been generated by {0} {1}, the statistical analysis tool"
                      " for git repositories.").format(
                          "<a href=\"https://github.com/renaultd/gitinspector\">gitinspector</a>",
                          version.__version__)
        cli_text = sys.argv
        cli_text[0] = "gitinspector.py"
        if "-o" in cli_text: # remove the output file
            ind = cli_text.index("-o")
            del cli_text[ind]
            del cli_text[ind]
        for r in runner.config.repositories: # remove the repositories
            if r in cli_text:
                cli_text.remove(r)
        cli_text = " ".join(cli_text)

        runner.out.writeln(
            html_header.format(title=_("Repository statistics for '{0}'").format(repos_string),
                               jquery_js=jquery_js,
                               d3_js=d3_js,
                               custom_js=custom_js,
                               style_css=style_css,
                               logo=logo.decode("utf-8", "replace"),
                               logo_text=logo_text,
                               repo_text=repos_text,
                               cli_text=cli_text,
                               show_minor_authors=_("Show minor authors"),
                               hide_minor_authors=_("Hide minor authors"),
                               show_minor_rows=_("Show rows with minor work"),
                               hide_minor_rows=_("Hide rows with minor work")))
    elif __selected_format__ == "json":
        runner.out.writeln("{\n\t\"gitinspector\": {")
        runner.out.writeln("\t\t\"version\": \"" + version.__version__ + "\",")

        if len(repos) <= 1:
            runner.out.writeln("\t\t\"repository\": \"" + repos_string + "\",")
        else:
            repos_json = "\t\t\"repositories\": [ "

            for repo in repos:
                repos_json += "\"" + repo.name + "\", "

            runner.out.writeln(repos_json[:-2] + " ],")

        runner.out.writeln("\t\t\"report_date\": \"" + time.strftime("%Y/%m/%d") + "\",")

    elif __selected_format__ == "xml":
        runner.out.writeln("<gitinspector>")
        runner.out.writeln("\t<version>" + version.__version__ + "</version>")

        if len(repos) <= 1:
            runner.out.writeln("\t<repository>" + repos_string + "</repository>")
        else:
            runner.out.writeln("\t<repositories>")

            for repo in repos:
                runner.out.writeln("\t\t<repository>" + repo.name + "</repository>")

            runner.out.writeln("\t</repositories>")

        runner.out.writeln("\t<report-date>" + time.strftime("%Y/%m/%d") + "</report-date>")
    else:
        repos_name = (repos_string if runner.config.branch == "master"
                     else "%s (branch %s)"%(repos_string, runner.config.branch))
        repos_text = (INFO_START_ONE_REPO() if len(repos) <= 1 else
                      INFO_START_MANY_REPOS()) + " " + \
                      repos_name + " " + INFO_MID_ANY_REPO() + " " + \
                      str(localization.get_date())

        runner.out.writeln(textwrap.fill(repos_text, width=terminal.get_size()[0]))

def output_footer(runner):
    """
    The function responsible for outputting a footer to the output.
    """
    if __selected_format__ == "html" or __selected_format__ == "htmlembedded":
        base = basedir.get_basedir()
        html_footer = __output_html_template__(base + "/templates/footer.html")
        runner.out.writeln(html_footer)
    elif __selected_format__ == "json":
        runner.out.writeln("\n\t}\n}")
    elif __selected_format__ == "xml":
        runner.out.writeln("</gitinspector>")
