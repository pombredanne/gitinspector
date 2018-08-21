from .outputable import Outputable
from .. import responsibilities as resp
import string
import datetime

from ..blame import Blame


class FileOwnerships(object):

    def __init__(self, changes):
        self.changes = changes
        self.owns = {}
        self.authors = {}

    def add(self, file, author, work, is_dir):
        if not(author in self.authors):
            self.authors[author] = self.changes.colors_by_author[author]
        sfile = file.split('/')
        if not(file in self.owns):
            self.owns[file] = { "work": {}, "parent": "", "is_dir" : is_dir }
        if not(author in self.owns[file]["work"]):
            self.owns[file]["work"][author] = work
        else:
            self.owns[file]["work"][author] += work
        sfile.pop()
        if (len(sfile) > 0):
            parent = "/".join(sfile)
            self.owns[file]["parent"] = parent
            self.add(parent, author, work, "true")

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
        ownerships = FileOwnerships(self.changes)
        for key,val in self.blames.blames.items():
            ownerships.add(key[1],key[0],val.rows,"false")

        with open("gitinspector/templates/test_output.html", 'r') as infile:
            src = string.Template( infile.read() )
            self.out.write(src.substitute(
                authors=ownerships.authors,
                ownerships=ownerships.owns,
            ))
        pass

    def output_text(self):
        pass

    def output_json(self):
        pass

    def output_xml(self):
        pass
