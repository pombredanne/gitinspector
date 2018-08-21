from .outputable import Outputable
from .. import responsibilities as resp
import string
import datetime

from ..blame import Blame


class TestOutput(Outputable):
    output_order = 120

    def __init__(self, runner):
        Outputable.__init__(self)
        self.changes = runner.changes
        self.blames = runner.blames
        self.weeks = runner.config.weeks
        self.display = True
        self.out = runner.out

    def output_html(self):
        authors = {}
        ownerships = {}
        for key,val in self.blames.blames.items():
            authors[key[0]] = self.changes.colors_by_author[key[0]]
            if not(key[1] in ownerships):
                ownerships[key[1]] = []
            ownerships[key[1]].append({
                "author": key[0],
                "rows": val.rows,
            })
        files = set(ownerships.keys())
        tree = set()
        for file in ownerships.keys():
            tree.add(file)
            sfile = file.split('/')
            if (len(sfile) > 1):
                dir = sfile.pop(0)
                for d in sfile:
                    tree.add(dir)
                    dir += "/" + d
        tree = sorted(list(tree))

        with open("gitinspector/templates/test_output.html", 'r') as infile:
            src = string.Template( infile.read() )
            self.out.write(src.substitute(
                authors=authors,
                tree=tree,
                ownerships=ownerships,
            ))
        pass

    def output_text(self):
        pass

    def output_json(self):
        pass

    def output_xml(self):
        pass
