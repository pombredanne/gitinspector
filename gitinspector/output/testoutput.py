from .outputable import Outputable
from .. import gravatar, timeline
import string

from ..blame import Blame


class TestOutput(Outputable):
    output_order = 120

    def __init__(self, runner):
        Outputable.__init__(self)
        self.changes = runner.changes
        self.weeks = runner.config.weeks
        self.display = True
        self.out = runner.out

    def output_html(self):
        data = timeline.TimelineData(self.changes, self.weeks)
        authors = [author[0] for author in data.get_authors()]
        entries = { a: {} for a in authors }
        for k, v in data.entries.items():
            author = k[0]
            period = k[1]
            entries[author][period] = [v.insertions, v.deletions, v.commits]

        timeline_dict = {
            "periods": data.get_periods(),
            "authors": authors,
            "changes": data.total_changes_by_period,
            "entries": entries,
        }

        with open("gitinspector/templates/test_output.html", 'r') as infile:
            src = string.Template( infile.read() )
            self.out.write(src.substitute(
                timeline=str(timeline_dict)
            ))
        pass

    def output_text(self):
        pass

    def output_json(self):
        pass

    def output_xml(self):
        pass
