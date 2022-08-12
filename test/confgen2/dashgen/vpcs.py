from dashgen.variables import *
from dashgen.confbase import *
from dashgen.confutils import *
from copy import deepcopy
import sys
class Vpcs(ConfBase):

    def __init__(self):
        self.dictname = 'vpc'
    
    def items(self):
        print('  Generating %s...' % self.dictname, file=sys.stderr)

        for eni_index in range(1, ENI_COUNT+1):
            IP_L = IP_L_START + (eni_index - 1) * IP_STEP4
            r_vpc = eni_index + ENI_L2R_STEP
            IP_R = IP_R_START + (eni_index - 1) * IP_STEP4
            
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

if __name__ == "__main__":
    conf=Vpcs()
    common_main(conf, dict_method=conf.toDict, list_method=conf.items)