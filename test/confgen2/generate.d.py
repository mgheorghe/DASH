#!/usr/bin/python3

import io, sys
import orjson
import yaml
import dashgen
import argparse
from dashgen.confbase import *
from dashgen.confutils import *

parser = commonArgParser()
args = parser.parse_args()

print('Generating config', file=sys.stderr)
enis = dashgen.enis.Enis()
aclgroups = dashgen.aclgroups.AclGroups()
vpcs = dashgen.vpcs.Vpcs()
vpcmappingtypes = dashgen.vpcmappingtypes.VpcMappingTypes()
vpcmappings = dashgen.vpcmappings.VpcMappings()
routingappliances = dashgen.routingappliances.RoutingAppliances()
routetables = dashgen.routetables.RouteTables()
prefixtags = dashgen.prefixtags.PrefixTags()

configs = [
        enis,
        aclgroups,
        vpcs,
        vpcmappingtypes,
        vpcmappings,
        routingappliances,
        routetables,
        prefixtags
]
log_memory("Generators instantiated")

def toDict(self=None):
        global configs
        c = {}
        for i in configs:
                c.update(i.toDict()) 
        log_memory("toDict()")
        return c

def toDictGen(self=None):
        global configs
        return {x.dictName():x.items() for x in configs}

def toList(self=None):
        return (c.items() for c in configs)

common_main(self=None, dict_method=toDictGen, list_method=toList)