from abc import ABC, abstractmethod
from copy import deepcopy
import os, sys
from dflt_params import *
class ConfBase(ABC):

    def __init__(self, name='base', params={}):
        self.dictname = name
        self.dflt_params = deepcopy(dflt_params)
        self.mergeParams(params)

    def mergeParams(self, params):
        self.params = deepcopy(self.dflt_params)
        # Merge provided params into/onto defaults
        self.params.update(params)
        # make scalar attributes for speed (compared to dict)
        for k,v in self.params.items():
            setattr(self, k, v)

        # print ("\n%s: %s\n" % (self.dictname, self.params), file=sys.stderr)

    @abstractmethod
    def items(self):
        pass

    def itemCount(self):
        return len(self.items())

    def dictName(self):
        return self.dictname

    def toDict(self):
        return {self.dictname: list(self.items())}

    def getParams():
        return self.params

    def pretty(self):
        pprint.pprint(self.toDict())
