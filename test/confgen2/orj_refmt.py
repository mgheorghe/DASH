#!/usr/bin/python3
#
# REad in tmp.json created by confgen2, emit file using orjson technique 
# per confgen so text can be compared to  ensure algorithm fidelity despite refactorings
import json
import orjson

print("Reading tmp.json...")
with open('tmp.json', 'r') as fpr:
    d=json.load(fpr)

print("Writing dash_conf.json...")

with open('dash_conf.json', 'wb') as fpw:
    fpw.write(orjson.dumps(d, option=orjson.OPT_INDENT_2))


