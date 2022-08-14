from abc import ABC, abstractmethod
from copy import deepcopy
import os, sys
from dflt_params import *
from munch import DefaultMunch
from datetime import datetime

class ConfBase(ABC):

    def __init__(self, name='base', params={}):
        self.dictname = name
        self.dflt_params = deepcopy(dflt_params)
        self.mergeParams(params)
        self.numYields = 0

    def mergeParams(self, params):
        # Merge provided params into/onto defaults
        self.params_dict = deepcopy(self.dflt_params)
        self.params_dict.update(params)

        # make scalar attributes for speed & brevity (compared to dict)
        # https://stackoverflow.com/questions/1305532/how-to-convert-a-nested-python-dict-to-object
        self.params = DefaultMunch.fromDict(self.params_dict)
        # print ('%s: self.params=' % self.dictname, self.params)


    @abstractmethod
    def items(self):
        pass

    # expensive - runs generator
    def itemCount(self):
        return len(self.items())

    def itemsGenerated(self):
        """ Last count of # yields, reset each time at begining"""
        return self.num_yields

    def dictName(self):
        return self.dictname

    def toDict(self):
        return {self.dictname: list(self.items())}

    def getParams(self):
        return self.params_dict

    def getMeta(self, message=''):
        """Generate metadata. FOr reference, could also add e.g. data to help drive tests"""
        return { 'meta': { 
                    'tstamp': datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                    'msg': message,
                    'params': self.getParams()
                }
            }

    def pretty(self):
        pprint.pprint(self.toDict())
