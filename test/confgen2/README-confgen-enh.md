# Improved generator-based confgen
## Features
* Generate complex DASH configurations, parameter driven
* Custom input params
* Output to file or stdio
* Select output format: JSON, yaml (future), none
* Generate all config (uber-generator) or just selected items (e.g. aclgroups)
* Potential to create custom apps to transform streaming data e.g into device API calls w/o intermediate text rendering
## High-level Diagram

![confgen-hld-diag](confgen-hld-diag.svg)

## Design
The uber-generator `generate.d.py` instantiates sub-generators and produces a composite output stream which can be rendered into text files (JSON) or sent to stdout for custom pipelines.

The uber-generator and sub-generators all derive from a base-class `ConfBase`. They all share a common `main` progam with CLI command-line options, which allows them to be used independently yet consistently.

The generators produce Python data structures which can be rendered into output text (e.g. JSON) or used to feed custom applications such as a saithrift API driver, to directly configure a device. Likewise a custom API driver can be developed for vendor-specific APIs.

Default parameters allow easy operations with no complex input. All parameters can be selectively overridden via cmd-line, input file or both.

## Sample CLI Usage
This may not be current; check latest for actual content.
```
$ ./generate.d.py -h
usage: generate.d.py [-h] [-f {json}] [-c {dict,list}] [-d] [-m] [-M "MSG"] [-P "{PARAMS}"] [-p PARAM_FILE]
                     [-o OFILE]

Generate DASH Configs

optional arguments:
  -h, --help            show this help message and exit
  -f {json}, --format {json}
                        Config output format.
  -c {dict,list}, --content {dict,list}
                        Emit dictionary (with inner lists), or list items only
  -d, --dump-params     Just dump parameters (defaults with user-defined merged in
  -m, --meta            Include metadata in output (only if "-c dict" used)
  -M "MSG", --msg "MSG"
                        Put MSG in metadata (only if "-m" used)
  -P "{PARAMS}", --set-params "{PARAMS}"
                        supply parameters as a dict, partial is OK; defaults and file-provided (-p)
  -p PARAM_FILE, --param-file PARAM_FILE
                        use parameter dict from file, partial is OK; overrides defaults
  -o OFILE, --output OFILE
                        Output file (default: standard output)

Usage:
=========
./generate.d.py                - generate output to stdout using uber-generator
./generate.d.py -o tmp.json    - generate output to file tmp.json
./generate.d.py -o /dev/null   - generate output to nowhere (good for testing)
./generate.d.py -c list        - generate just the list items w/o parent dictionary
dashgen/aclgroups.py [options] - run one sub-generator, e.g. acls, routetables, etc.
                               - many different subgenerators available, support same options as uber-generator

Passing parameters. Provided as Python dict, see dflt_params.py for available items
================
./generate.d.py -d                          - display default parameters and quit
./generate.d.py -d -P PARAMS                - override given parameters, display and quit; see dflt_params.py for template
./generate.d.py -d -p PARAM_FILE            - override parameters in file; display only
./generate.d.py -d -p PARAM_FILE -P PARAMS  - override params from file, then override params from cmdline; display only
./generate.d.py -p PARAM_FILE -P PARAMS     - override params from file, then override params from cmdline, generate output

Examples:
./generate.d.py -d -p params_small.py -P "{'ENI_COUNT': 16}"  - use params_small.py but override ENI_COUNT; display params
./generate.d.py -p params_hero.py -o tmp.json                 - generate full "hero test" scale config as json file
dashgen/vpcmappingtypes.py -m -M "Kewl Config!"               - generate dict of vpcmappingtypes, include meta with message            
```
## Confgen Applications
Two anticipated applications (see Figure below):
* Generate a configuration file, e.g. JSON, and use this to feed downstream tools such as a DUT configuration utility.
* Use the output of the config data stream generators to perform on-the-fly DUT configuration without intermediate JSON file rendering; also configure traffic-generators using data in the config info itself.

![confgen-apps](confgen-apps.svg)

# TODO
* Reconcile the param dicts vs. param attributes obtained via Munch, use of scalar variables inside performance-heavy loops etc. There is a tradeoff between elegance, expressiveness and performance.
# IDEAS/Wish-List
* Expose yaml format, need to work on streaming output (bulk output was owrking but slow).
* Use logger instead of print to stderr
* logging levels -v, -vv, -vvv etc., otherwise silent on stderr
* -O, --optimize flags for speed or memory (for speed - expand lists in-memory and use orjson serializer, like original code)
* Use nested generators inside each sub-generator, instead of nested loops, to reduce in-memory usage; may require enhancing JSON output streaming to use recursion etc.
## Comparisons - confgen, confgen2

### confgen - original design
Note I added some memory usage logging
```
chris@chris-z4:~/chris-DASH/DASH/test/confgen$ time ./generate.d.py 
Start: Memory: 11.7 MB, 
generating config
    enis.py
enis.generate() done: Memory: 11.7 MB, 
    aclgroups.py
aclgroups.generate() done: Memory: 1065.6 MB, 
    vpc.py
vpc.generate() done: Memory: 1065.6 MB, 
    vpcmappingtypes.py
vpcmappingtypes.generate() done: Memory: 1065.6 MB, 
    vpcmappings.py
vpcmappings.generate() done: Memory: 1997.9 MB, 
    routingappliances.py
routingappliances.generate() done: Memory: 1997.9 MB, 
    routetables.py
routetables.generate() done: Memory: 2257.6 MB, 
    prefixtags.py
prefixtags.generate() done: Memory: 2257.6 MB, 
config.update( all ) done: Memory: 2257.6 MB, 
writing the config to file
File write done: Memory: 3567.9 MB, 
done

real	1m15.912s
user	1m14.006s
sys	0m1.904s
```
## confgen2
```
chris@chris-z4:~/chris-DASH/DASH/test/confgen2$ time python3 generate.d.py -f json  -c dict -o dict_hero.json
Generating config
Generators instantiated: Memory: 14.0 MB, 
Start: Memory: 14.0 MB, 
  Generating vpc-mappings-routing-types...
writeDictFileIter enter: Memory: 14.0 MB, 
Writing the json config to dict_hero.json...
  Generating enis...
wrote dict item 'enis': Memory: 14.1 MB, 
  Generating acl-groups...
items() exit: Memory: 84.4 MB, 
wrote dict item 'acl-groups': Memory: 84.4 MB, 
  Generating vpc...
wrote dict item 'vpc': Memory: 84.4 MB, 
wrote dict item 'vpc-mappings-routing-types': Memory: 84.4 MB, 
  Generating vpc-mappings...
wrote dict item 'vpc-mappings': Memory: 324.0 MB, 
  Generating routing-appliances...
wrote dict item 'routing-appliances': Memory: 324.0 MB, 
  Generating route-tables...
wrote dict item 'route-tables': Memory: 324.0 MB, 
  Generating prefix-tags...
wrote dict item 'prefix-tags': Memory: 324.0 MB, 
writeDictFileIter exit: Memory: 324.0 MB, 
Done: Memory: 324.0 MB, 

real	1m34.455s
user	1m32.602s
sys	0m1.462s
```
