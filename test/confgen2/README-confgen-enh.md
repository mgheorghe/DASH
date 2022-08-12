# Improved generator-based confgen

# TODOs
* Expose yaml format, need to work on streaming output (bulk output was owrking but slow).
# IDEAS/Wish-List
* Base class defines output serialization methods (or uses plug-in helper) to emit JSON, write to file, perform SAI API calls (event listener using streaming emitter?), etc.
* __main__ function allows driving from cmd-line for experiments
* __init__ accepts mix of kwargs, dict or json to assign params. Can use a global json for all generators or override selectively
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
