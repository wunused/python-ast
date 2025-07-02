import italian as i
from french import french
from protogermanic import protogermanic as pg

class english(pg, i.italian, french):
    def language():
        pass
    def equirks():
        pass

e = english()
