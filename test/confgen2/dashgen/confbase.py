from abc import ABC, abstractmethod

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
        # return {self.dictname: (x for x in self.items())}

    def pretty(self):
        pprint.pprint(self.toDict())
