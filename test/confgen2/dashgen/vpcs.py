#!/usr/bin/python3

from variables import *
from confbase import *
from confutils import *
from copy import deepcopy
import sys
class Vpcs(ConfBase):

    def __init__(self, params={}):
        super().__init__('vpc', params)
    
    def items(self):
        self.numYields = 0
        print('  Generating %s...' % self.dictname, file=sys.stderr)
        p=self.params

        for eni_index in range(1, p.ENI_COUNT+1):
            IP_L = IP_L_START + (eni_index - 1) * IP_STEP4
            r_vpc = eni_index + ENI_L2R_STEP
            IP_R = IP_R_START + (eni_index - 1) * IP_STEP4
            
            self.numYields+=1
            yield \
                {
                    "VPC:%d" % eni_index: {
                        "vpc-id": "vpc-%d" % eni_index,
                        "vni-key": eni_index,
                        "encap": "vxlan",
                        "address_spaces": [
                            "%s/32" % IP_L
                        ]
                    },
                }

            self.numYields+=1
            yield \
                {
                    "VPC:%d" % r_vpc: {
                        "vpc-id": "vpc-%d" % r_vpc,
                        "vni-key": r_vpc,
                        "encap": "vxlan",
                        "address_spaces": [
                            "%s/9" % IP_R
                        ]
                    },
                }
        log_memory('    %s: generated %d items' % (self.dictname, self.numYields))

if __name__ == "__main__":
    conf=Vpcs()
    common_main(conf)