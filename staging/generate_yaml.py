import os
from copy import deepcopy
from collections import defaultdict
from templates import *

data = dict()
cats = defaultdict(set)    # modules by category

def module(name, url, desc, license):
    return dict(name=name, url=url, description=desc, license=license)

modules = [module(*line.rstrip().split('\t')) for line in open('data.tsv')]

for m in modules: 
    m['tags'] = set()
    m['categories'] = set()
    data[m['name']] = m

for row in open('categories.tsv'):
    (cat, modules) = row.rstrip().split('\t')
    for m in modules.split(', '):
        try:
            data[m]['categories'].add(cat)
            cats[cat].add(m)
        except KeyError:
            print m, "<<<<<<<< CAT"

for row in open('cat-tagging.tsv'):
    (tags, modules) = row.rstrip().split('\t')
    for tag in tags.split(', '):
        for m in modules.split(', '):
            try:
                data[m]['tags'].add(tag)
            except KeyError:
                print m, "<<<<<<<< CAT-TAG"

for row in open('tags.tsv'):
    (tag, modules) = row.rstrip().split('\t')
    for m in modules.split(', '):
        try:
            data[m]['tags'].add(tag)
        except KeyError:
            print m, "<<<<<<<< TAG"

versions = dict()

for row in open('versions.tsv'):
    (name, vers) = row.rstrip().split('\t')
    versions[name] = vers.split(', ')


import os
from glob import glob
import subprocess

moduledir="/software/modulefiles"
yamldir="yamlfiles"
for module in glob(moduledir+"/*/*"):
    softname = os.path.basename(os.path.dirname(module))
    modulevers = os.path.basename(module)

    if not softname in data:
        print softname
        continue

    if "+" in modulevers:
        softvers, compiler = modulevers.split('+', 1)
        compiler = compiler.replace("-", "/", 1)
    else:
        softvers = modulevers
        compiler = ""

    data[softname]['version'] = softvers
    data[softname]['compiler'] = compiler

    cmd = "sed -n -e 's/^module load //p' " + module
    dependencies = subprocess.check_output(cmd, shell=True)
    data[softname]['dependencies'] = ",".join(dependencies.split())

    data[softname]['tags'] = ",".join(data[softname]['tags'])
    data[softname]['categories'] = ",".join(data[softname]['categories'])

    try:
        os.mkdir(yamldir+"/"+softname)
    except OSError:
        pass

    with open(yamldir+"/"+softname+"/"+modulevers+".yaml","w") as yml:
        print >>yml, module_version_yaml.format(**data[softname])
