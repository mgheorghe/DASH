#!/usr/bin/python3

from variables import *
from confbase import *
from confutils import *
import sys
class PrefixTags(ConfBase):

    def __init__(self, params={}):
        super().__init__('prefix-tags', params)

    def items(self):
        print('  Generating %s...' % self.dictname, file=sys.stderr)
        for eni_index in range(1, self.ENI_COUNT+1):
            IP_L = IP_L_START + (eni_index - 1) * IP_STEP4
            r_vpc = eni_index + ENI_L2R_STEP
            IP_R = IP_R_START + (eni_index - 1) * IP_STEP4
            yield \
                {
                    "PREFIX-TAG:VPC:%d" % eni_index: {
                        "prefix-tag-id": "%d" % eni_index,
                        "prefix-tag-number": eni_index,
                        "ip-prefixes-ipv4": [
                            "%s/32" % IP_L
                        ]
                    },
                }
            yield \
                {
                    "PREFIX-TAG:VPC:%d" % r_vpc: {
                        "prefix-tag-id": "%d" % r_vpc,
                        "prefix-tag-number": r_vpc,
                        "ip-prefixes-ipv4": [
                            "%s/9" % IP_R
                        ]
                    },
                }
            
if __name__ == "__main__":
    conf=PrefixTags()
    common_main(conf)