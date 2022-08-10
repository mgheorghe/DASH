import ipaddress
import orjson
import io
import pprint
from abc import ABC, abstractmethod

from dashgen.variables import *
class ConfBase(ABC):
    # DICTNAME='base-class'

    def __init__(self):
        self.dictname = 'base-class'
        pass

    @abstractmethod
    def items(self):
        pass

    def itemCount(self):
        return len(self.items())

    def dictName(self):
        return self.dictname

    def toDict(self):
        return {self.dictname: list(self.items())}

    def pretty(self):
        pprint.pprint(self.toDict())

    def toFile(self,filename):
        with io.open(filename, 'wb') as jsonfile:
            jsonfile.write(orjson.dumps(self.toDict(), option=orjson.OPT_INDENT_2))        
