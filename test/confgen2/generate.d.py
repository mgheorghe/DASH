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

class DashConfig(ConfBase):

        def __init__(self, params={}):
                super().__init__('dash-config', params)

        def generate(self):
                enis = dashgen.enis.Enis(self.params)
                aclgroups = dashgen.aclgroups.AclGroups(self.params)
                vpcs = dashgen.vpcs.Vpcs(self.params)
                vpcmappingtypes = dashgen.vpcmappingtypes.VpcMappingTypes(self.params)
                vpcmappings = dashgen.vpcmappings.VpcMappings(self.params)
                routingappliances = dashgen.routingappliances.RoutingAppliances(self.params)
                routetables = dashgen.routetables.RouteTables(self.params)
                prefixtags = dashgen.prefixtags.PrefixTags(self.params)

                self.configs = [
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

                # This instantiates config in-memory - could use if want to output with orjson for speed
                # def toDict(self):
                #         c = {}
                #         for i in self.configs:
                #                 c.update(i.toDict()) 
                #         log_memory("toDict()")
                #         return c

        def toDict(self):
                return {x.dictName():x.items() for x in self.configs}

        def items(self):
                return (c.items() for c in self.configs)

if __name__ == "__main__":
    conf=DashConfig()
    common_parse_args(conf)

    log_memory("Start")
    conf.generate()
    common_output(conf)
    log_memory("Done")
