from .outputable import Outputable
from .. import gravatar, timeline

import os
import string
import datetime

from ..blame import Blame


class ActivityOutput(Outputable):
    output_order = 120

    def __init__(self, runner):
        Outputable.__init__(self)
        self.changes = runner.changes
        self.blames = runner.blames
        self.weeks = runner.config.weeks
        self.display = bool(runner.changes.commits) and runner.config.timeline
        self.out = runner.out

    def output_html(self):
        data = timeline.TimelineData(self.changes, self.weeks)

        if self.weeks:
            periods = [ [d, datetime.datetime.strptime(d + "-1", "%YW%U-%w")]
                        for d in data.get_periods()]
            first_period = periods[0][1]
            periods = [ [d[0], int((d[1]-first_period).days / 7)] \
                        for d in periods ]
        else:
            periods = [ [d, datetime.datetime.strptime(d, "%Y-%m")] for d in data.get_periods()]
            first_period = periods[0][1]
            periods = [ [d[0], (d[1].year-first_period.year)*12 + (d[1].month-first_period.month)] \
                        for d in periods ]
        max_period = periods[-1][1]
        periods = { k[0]: k[1] for k in periods }
        max_work   = max([el[1][2] for el in list(data.total_changes_by_period.items())])
        entries = { p: [] for p in periods.keys() }
        for k, v in data.entries.items():
            author = k[0]
            period = k[1]
            entries[period].append({ "author": author,
                                     "work": v.insertions + v.deletions,
                                     "commit": [v.insertions, v.deletions, v.commits]})
        total_changes = {k: v[2] for k, v in data.total_changes_by_period.items()}

        sorted_authors = { a: self.changes.colors_by_author[a]
                           for a in self.changes.authors_by_responsibilities() }
        timeline_dict = {
            "periods": periods,
            "max_period": max_period,
            "max_work": max_work,
            "authors": sorted_authors,
            "changes": total_changes,
            "entries": entries,
        }

        temp_file = os.path.join(os.path.dirname(__file__),
                                 "../templates/activity_output.html")
        with open(temp_file, 'r') as infile:
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
