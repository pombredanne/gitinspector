from .outputable import Outputable
from .. import gravatar, timeline
import string
import datetime

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
        if self.weeks:
            periods = [ [d, datetime.datetime.strptime(d + "-1", "%YW%W-%w")] for d in data.get_periods()]
            first_period_y = periods[0][1].year
            first_period_w = int(periods[0][0][-2:])
            periods = [ [d[0], (d[1].year-first_period_y)*53 + (int(d[0][-2:])-first_period_w)] \
                        for d in periods ]
        else:
            periods = [ [d, datetime.datetime.strptime(d, "%Y-%m")] for d in data.get_periods()]
            first_period = periods[0][1]
            periods = [ [d[0], (d[1].year-first_period.year)*12 + (d[1].month-first_period.month)] \
                        for d in periods ]
        authors = [author[0] for author in data.get_authors()]
        entries = { a: {} for a in authors }
        for k, v in data.entries.items():
            author = k[0]
            period = k[1]
            entries[author][period] = [v.insertions, v.deletions, v.commits]

        timeline_dict = {
            "periods": periods,
            "max_period": periods[-1][1],
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
