from .outputable import Outputable
from .. import gravatar
import string

from ..blame import Blame


class TestOutput(Outputable):
    output_order = 120

    def __init__(self, runner):
        Outputable.__init__(self)
        self.changes = runner.changes
        self.blames = runner.blames
        self.display = True
        self.out = runner.out

    def output_html(self):
        pass

    def output_text(self):
        pass

    def output_json(self):
        pass

    def output_xml(self):
        pass
