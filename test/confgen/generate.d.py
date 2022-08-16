#!/usr/bin/python3

import io, sys
# import orjson
# import yaml
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
                # Pass top-level params to sub-generrators.
                # Future - can pass some overridden values if needed.
                enis = dashgen.enis.Enis(self.params_dict)
                aclgroups = dashgen.aclgroups.AclGroups(self.params_dict)
                vpcs = dashgen.vpcs.Vpcs(self.params_dict)
                vpcmappingtypes = dashgen.vpcmappingtypes.VpcMappingTypes(self.params_dict)
                vpcmappings = dashgen.vpcmappings.VpcMappings(self.params_dict)
                routingappliances = dashgen.routingappliances.RoutingAppliances(self.params_dict)
                routetables = dashgen.routetables.RouteTables(self.params_dict)
                prefixtags = dashgen.prefixtags.PrefixTags(self.params_dict)

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
