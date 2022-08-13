import sys,resource, time
import orjson
import collections, itertools, json
import yaml
import io, sys
import pprint
import argparse,textwrap


def log_memory(msg=''):
    if "linux" in sys.platform.lower():
        to_MB = 1024
    else:
        to_MB = 1024 * 1024
    print("%s: Memory: %.1f MB, " % (msg,
        resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / to_MB),file=sys.stderr)


# From https://stackoverflow.com/questions/12670395/json-encoding-very-long-iterators
class IterEncoder(json.JSONEncoder):
    """
    JSON Encoder that encodes iterators as well.
    Write directly to file to use minimal memory
    """
    class FakeListIterator(list):
        def __init__(self, iterable):
            self.iterable = iter(iterable)
            try:
                self.firstitem = next(self.iterable)
                self.truthy = True
            except StopIteration:
                self.truthy = False

        def __iter__(self):
            if not self.truthy:
                return iter([])
            return itertools.chain([self.firstitem], self.iterable)

        def __len__(self):
            raise NotImplementedError("Fakelist has no length")

        def __getitem__(self, i):
            raise NotImplementedError("Fakelist has no getitem")

        def __setitem__(self, i):
            raise NotImplementedError("Fakelist has no setitem")

        def __bool__(self):
            return self.truthy

    def default(self, o):
        if isinstance(o, collections.abc.Iterable):
            return type(self).FakeListIterator(o)
        return super().default(o)

def writeListFileIter(config, format, filename='<stdout>'):
    log_memory("writeListFileIter enter")
    if filename == '<stdout>':
        writeListFpIter(config, format, sys.stdout)
    else:
        with open(filename, "wt") as file:
            writeListFpIter(config, format, fp)
    log_memory("writeListFileIter exit")

def writeListFpIter(config, format, fp):
    log_memory("writeListFpIter enter")
    if format == 'json':
        json.dump(config, fp, cls=IterEncoder,indent = 2, separators=(',', ': '))
    else:
        raise NotImplementedError('ERROR: unsupported format %s' % format)
    log_memory("writeListFpIter exit")


def writeDictFileIter(config, format, filename='<stdout>'):
    log_memory("writeDictFileIter enter")

    def _writeDictFileIter(config, fp):
        fp.write('{\n')
        first = True
        for key, list in config.items():
            if not first:
                fp.write(',\n')
            fp.write('  "%s":\n' % key)
            json.dump(list, fp, cls=IterEncoder,indent = 2, separators=(',', ': '))
            first = False
            log_memory("wrote dict item '%s'" % key)
        fp.write('\n}\n')

    if format == 'json':
            print('Writing the %s config to %s...' % (format, filename), file=sys.stderr)
            if filename == '<stdout>':
                fp = sys.stdout
                _writeDictFileIter(config, fp)
            else:
                with open(filename, 'wt') as fp:
                    _writeDictFileIter(config, fp)
    else:
        raise NotImplementedError('ERROR: unsupported format %s' % format)

    log_memory("writeDictFileIter exit")

def commonArgParser():
    parser = argparse.ArgumentParser(description='Generate DASH Configs',
                formatter_class=argparse.RawTextHelpFormatter,
                epilog = textwrap.dedent('''
Examples:
=========
./generate.d.py                - generate output to stdout using uber-generator
./generate.d.py -o tmp.json    - generate output to file tmp.json
./generate.d.py -o /dev/null   - generate output to nowhere (good for testing)
./generate.d.py -c list        - generate just the list items w/o parent dictionary
dashgen/aclgroups.py [options] - run one sub-generator, e.g. acls, routetables, etc.
                               - many different subgenerators available, support same options as uber-generator

Passing scale and other parameters:
./generate.d.py -d                   - display default parameters and quit
./generate.d.py -d -P "{...}"        - override some parameters, display and quit; see dflt_params.py for template
./generate.d.py -P "{...}" [opts]    - override some parameters generate output

Example:
./generate.d.py -d -P "{'ACL_RULES_NSG': 3, 'ACL_TABLE_COUNT': 1000, 'ENI_COUNT': 8}"
./generate.d.py -P "{'ACL_RULES_NSG': 3, 'ACL_TABLE_COUNT': 1000, 'ENI_COUNT': 8}" -o tmp.json




            '''))

    # parser.add_argument('-f', '--format', choices=['json', 'yaml'], default='json',
    parser.add_argument('-f', '--format', choices=['json'], default='json',
            help='Config output format.')

    parser.add_argument('-c', '--content', choices=['dict', 'list'], default='dict',
            help='Emit dictionary (with inner lists), or list items only')

    parser.add_argument('-d', '--dump-params', action='store_true',
            help='Just dump paramters (defaults with user-defined merged in')

    parser.add_argument('-P', '--set-params', metavar='{PARAMS}',
            help='supply parameters as a dict, partial is OK')

    parser.add_argument('-p', '--param-file', metavar='PARAM_FILE',
            help='use parameter dict from file, partial is OK')

    parser.add_argument(
            '-o', '--output', default='<stdout>', metavar='OFILE',
            help="Output file (default: standard output)")

    return parser

def common_parse_args(self):
    parser = commonArgParser()
    self.args = parser.parse_args()

    if self.args.set_params:
        self.mergeParams(eval(self.args.set_params))

    if self.args.dump_params:
        print(self.params)
        exit()

def common_output(self):
    if self.args.content == 'dict':
        writeDictFileIter(self.toDict(), self.args.format, self.args.output)
    else:
        writeListFileIter(self.items(), self.args.format, self.args.output)

def common_main(self):
    common_parse_args(self)

    log_memory("Start")
    common_output(self)
    log_memory("Done")
