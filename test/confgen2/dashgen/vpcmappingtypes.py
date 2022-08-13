#!/usr/bin/python3

from variables import *
from confbase import *
from confutils import *
import sys
class VpcMappingTypes(ConfBase):

    def __init__(self, params={}):
        super().__init__('vpc-mappings-routing-types', params)
    
    def items(self):
        print('  Generating %s...' % self.dictname, file=sys.stderr)
        vpcmappingtypes = [
            "vpc",
            "privatelink",
            "privatelinknsg"
        ]

        # return list, not generator
        return vpcmappingtypes

if __name__ == "__main__":
    conf=VpcMappingTypes()
    common_main(conf)