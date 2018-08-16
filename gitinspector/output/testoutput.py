from .outputable import Outputable
from .. import gravatar
import string

from ..blame import Blame

class TestOutput(Outputable):
    output_order = 110

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

        for entry in author_list:
            authorinfo = authorinfo_dict.get(entry)
            percentage = 0 if total_changes == 0 else \
                (authorinfo.insertions + authorinfo.deletions) / total_changes * 100

            data_array.append({
                "avatar": "<img src=\"{0}\"/>".format(gravatar.get_url(self.changes.get_latest_email_by_author(entry))),
                "color": self.changes.colors_by_author[entry],
                "name":  entry,
                "commits" : authorinfo.commits,
                "insertions" : authorinfo.insertions,
                "deletions" : authorinfo.deletions,
                "changes" : "{0:.2f}".format(percentage),
                })

        with open("gitinspector/html/test_output.html", 'r') as infile:
            src = string.Template( infile.read() )
            self.out.write(src.substitute(
                changes_data=str(data_array),
            ))

    def output_text(self):
        pass

    def output_json(self):
        pass

    def output_xml(self):
        pass


class TestOutput2(Outputable):
    output_order = 120

    def __init__(self, runner):
        Outputable.__init__(self)
        self.changes = runner.changes
        self.blames = runner.blames
        self.display = True
        self.out = runner.out

    def output_html(self):
        blames_list = list(self.blames.get_summed_blames().items())
        blames_list.sort(key=lambda x: x[1].rows, reverse=True)
        total_blames = 0
        for i in blames_list:
            total_blames += i[1].rows

        data_array = []

        for entry in blames_list:
            name = entry[0]
            data_array.append({
                "avatar": "<img src=\"{0}\"/>".format(gravatar.get_url(self.changes.get_latest_email_by_author(name))),
                "color": self.changes.colors_by_author[name],
                "name":  name,
                "rows": entry[1].rows,
                "stability": "{0:.1f}".format(Blame.get_stability(name, entry[1].rows, self.changes)),
                "age": "{0:.1f}".format(float(entry[1].skew) / entry[1].rows),
                "comments": "{0:.2f}".format(100.0 * entry[1].comments / entry[1].rows),
            })

        with open("gitinspector/html/test_output2.html", 'r') as infile:
            src = string.Template( infile.read() )
            self.out.write(src.substitute(
                remains_data=str(data_array),
            ))

    def output_text(self):
        pass

    def output_json(self):
        pass

    def output_xml(self):
        pass
