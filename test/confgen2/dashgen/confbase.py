import ipaddress
import orjson
import yaml
import io, sys
import pprint
from abc import ABC, abstractmethod
import argparse,textwrap

from dashgen.variables import *
class ConfBase(ABC):
    # DICTNAME='base-class'

    def __init__(self):
        self.dictname = 'base-class'
        pass

    @abstractmethod
    def items(self):
        pass

    def itemCount(self):
        return len(self.items())

    def dictName(self):
        return self.dictname

    def toDict(self):
        return {self.dictname: list(self.items())}
        # return {self.dictname: (x for x in self.items())}

    def pretty(self):
        pprint.pprint(self.toDict())

    def toJsonFile(self,filehandle=sys.stdout):
        print('Writing the JSON %s config to %s...' % (self.dictName, filehandle.name), file=sys.stderr)
        if filehandle.name == '<stdout>':
            # content is binary, convert to text, send to stdout
            filehandle.write(orjson.dumps(self.toDict(), option=orjson.OPT_INDENT_2).decode(encoding='utf-8'))
            print("")
        else:
            # write binary content to file
            filehandle.write(orjson.dumps(self.toDict(), option=orjson.OPT_INDENT_2))

    def toYamlFile(self, filehandle=sys.stdout):
        print('Writing the YAML %s config to %s...' % (self.dictName, filehandle.name), file=sys.stderr)
        yaml.dump(config, filehandle)

# Non-class utillity methods

def writeDictFile(config, format, filename='<stdout>'):
    if format == 'json':
            print('Writing the %s config to %s...' % (format, filename), file=sys.stderr)
            if filename == '<stdout>':
                    # content is binary, convert to text, send to stdout
                    sys.stdout.write(orjson.dumps(config, option=orjson.OPT_INDENT_2).decode(encoding='utf-8'))
                    sys.stdout.write('\n')
            else:
                    with open(filename, 'wb') as file:
                            # write binary content to file
                            file.write(orjson.dumps(config, option=orjson.OPT_INDENT_2))

    elif format == 'yaml':
            print('Writing the %s config to %s...' % (format, filename), file=sys.stderr)
            if filename == '<stdout>':
                    yaml.dump(config, sys.stdout)
            else:
                    with open('filename', 'w') as file:
                            # write binary content to file
                            yaml.dump(config, file)
    else:
            print('ERROR: unknown format %s' % format, file=sys.stderr)

def writeListFile(config, format, filename='<stdout>'):
    # writeDictFile(config, format, filename)
    if format == 'json':
            print('Writing the %s config to %s...' % (format, filename), file=sys.stderr)
            if filename == '<stdout>':
                    # content is binary, convert to text, send to stdout
                    sys.stdout.write('[\n')
                    first = True
                    for item in config:
                        if not first:
                            sys.stdout.write(',\n')
                        sys.stdout.write(orjson.dumps(item, option=orjson.OPT_INDENT_2).decode(encoding='utf-8'))
                        first = False
                    sys.stdout.write('\n]\n')
            else:
                    with open(filename, 'wb') as file:
                            # write binary content to file
                            file.write(orjson.dumps(config, option=orjson.OPT_INDENT_2))


def commonArgParser():
    parser = argparse.ArgumentParser(description='Generate DASH Configs',
                formatter_class=argparse.RawTextHelpFormatter,
                epilog = textwrap.dedent('''
Examples:
=========
./generate.d.py -o tmp.json   - generate output to file tmp.json
./generate.d.py               - generate output to stdout
            '''))

    parser.add_argument('-f', '--format', choices=['json', 'yaml'], default='json',
            help='Config output format.')

    parser.add_argument('-c', '--content', choices=['dict', 'list'], default='dict',
            help='Emit dictionary (with inner lists), or list items only')

    parser.add_argument(
            '-o', '--output', default='<stdout>',
            metavar='PATH',
            help="Output file (default: standard output)")

    return parser

def common_main(self=None, dict_method=None, list_method=None):
    parser = commonArgParser()
    args = parser.parse_args()
    if args.content == 'dict':
        writeDictFile(dict_method(), args.format, args.output)
    else:
        writeListFile(list_method(), args.format, args.output)

    print('Done', file=sys.stderr)