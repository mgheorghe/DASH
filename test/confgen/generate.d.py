#!/usr/bin/python3
import io
import orjson
import dashgen
from dashgen.confutils import log_memory as log_memory

log_memory("Start")

print('generating config')
enis = dashgen.enis.generate()
log_memory("enis.generate() done")

aclgroups = dashgen.aclgroups.generate()
log_memory("aclgroups.generate() done")

vpc = dashgen.vpc.generate()
log_memory("vpc.generate() done")

vpcmappingtypes = dashgen.vpcmappingtypes.generate()
log_memory("vpcmappingtypes.generate() done")

vpcmappings = dashgen.vpcmappings.generate()
log_memory("vpcmappings.generate() done")

routingappliances = dashgen.routingappliances.generate()
log_memory("routingappliances.generate() done")

routetables = dashgen.routetables.generate()
log_memory("routetables.generate() done")

prefixtags = dashgen.prefixtags.generate()
log_memory("prefixtags.generate() done")

config = {}
config.update(enis)
config.update(aclgroups)
config.update(vpc)
config.update(vpcmappingtypes)
config.update(vpcmappings)
config.update(routingappliances)
config.update(routetables)
config.update(prefixtags)

log_memory("config.update( all ) done")

print('writing the config to file')
with io.open(r'dash_conf.json', 'wb') as jsonfile:
    jsonfile.write(orjson.dumps(config, option=orjson.OPT_INDENT_2))
log_memory("File write done")

print('done')
