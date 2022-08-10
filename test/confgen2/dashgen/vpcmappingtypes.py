from dashgen.variables import *
from dashgen.confbase import *
import sys
class VpcMappingTypes(ConfBase):

    def __init__(self):
        self.dictname = 'vpc-mappings-routing-types'
    
    def items(self):
        print('  Generating %s...' % self.dictname, file=sys.stderr)
        # Note double list to match original confgen
        vpcmappingtypes = [[
            "vpc",
            "privatelink",
            "privatelinknsg"
        ]]

        # return list, not generator
        return vpcmappingtypes

if __name__ == "__main__":
    conf=VpcMappingTypes()
    conf.pretty()