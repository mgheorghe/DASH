#!/usr/bin/python3

import io, sys
import orjson
import dashgen
import argparse
import textwrap


parser = argparse.ArgumentParser(description='Generate DASH Configs',
            formatter_class=argparse.RawTextHelpFormatter,
            epilog = textwrap.dedent('''
Examples:
=========
./generate.d.py -o tmp.json   - generate output to file tmp.json
./generate.d.py               - generate output to stdout
            '''))
            
parser.add_argument('-f', '--format', choices=['json'], default='json',
        help='Config output format.')

parser.add_argument(
        '-o', '--output', type=argparse.FileType('wb'), default=sys.stdout,
        metavar='PATH',
        help="Output file (default: standard output)")

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

# TODO - use streaming JSON dict-by-dict
config = {}
config.update(enis.toDict())
config.update(aclgroups.toDict())
config.update(vpcs.toDict())
config.update(vpcmappingtypes.toDict())
config.update(vpcmappings.toDict())
config.update(routingappliances.toDict())
config.update(routetables.toDict())
config.update(prefixtags.toDict())

output = args.output
if output.name == '<stdout>':
    # content is binary, convert to text, send to stdout
   output.write(orjson.dumps(config, option=orjson.OPT_INDENT_2).decode(encoding='utf-8'))
   print("")
else:
    # write binary content to file
    print('Writing the config to %s...' % output.name, file=sys.stderr)
    output.write(orjson.dumps(config, option=orjson.OPT_INDENT_2))

print('done', file=sys.stderr)
