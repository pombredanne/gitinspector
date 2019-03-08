from .outputable import Outputable

import os
import string


class FileOwnerships(object):

    def __init__(self, changes):
        self.changes = changes
        self.owns = {}
        self.committers = {}

    def add(self, file, committer, work, is_dir):
        js_committer = committer[0] + " " + committer[1] # JS does not handle pairs
        if not(js_committer in self.committers):
            self.committers[js_committer] = self.changes.committers[committer]["color"]
        sfile = file.split('/')
        if not(file in self.owns):
            self.owns[file] = { "work": {}, "parent": "", "is_dir" : is_dir, "name" : sfile[-1] }
        if not(js_committer in self.owns[file]["work"]):
            self.owns[file]["work"][js_committer] = work
        else:
            self.owns[file]["work"][js_committer] += work
        sfile.pop()
        if (len(sfile) > 0):
            parent = "/".join(sfile)
            self.owns[file]["parent"] = parent
            self.add(parent, committer, work, "true")

    def compute_max_work(self):
        if not self.owns.values():
            return 0
        else:
            return max([ w for o in self.owns.values()
                         for w in o["work"].values() ])


class OwnershipOutput(Outputable):
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
        max_work = ownerships.compute_max_work()

        temp_file = os.path.join(os.path.dirname(__file__),
                                 "../templates/ownership_output.html")
        with open(temp_file, 'r') as infile:
            src = string.Template( infile.read() )
            self.out.write(src.substitute(
                authors=ownerships.committers,
                ownerships=ownerships.owns,
                max_work=max_work,
            ))
        pass

    def output_text(self):
        pass

    def output_json(self):
        pass

    def output_xml(self):
        pass
