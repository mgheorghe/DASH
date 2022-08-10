#!/usr/bin/python3

import io, sys
import orjson
import yaml
import dashgen
import argparse

parser = dashgen.confbase.commonArgParser()
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

# config = {}
# config.update(enis.toDict())
# config.update(aclgroups.toDict())
# config.update(vpcs.toDict())
# config.update(vpcmappingtypes.toDict())
# config.update(vpcmappings.toDict())
# config.update(routingappliances.toDict())
# config.update(routetables.toDict())
# config.update(prefixtags.toDict())

def toDict(self=None):
        global configs
        c = {}
        for i in configs:
                c.update(i.toDict()) 
        return c

def toList(self=None):
        return (c.items() for c in configs)

dashgen.confbase.common_main(self=None, dict_method=toDict, list_method=toList)