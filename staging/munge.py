import os
import rst_template

data = dict()

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


yaml = '''
name: {name}
description: "{description}"
version: {version}
compiler: {compiler}
license: {license}
categories: {categories}
tags: {tags}
url: {url}
usage: >
    Use the `module system
    <https://rcc.uchicago.edu/docs/software/index.html#using-software-modules>`_
    to load this version of {name}::
    
        module load {name}/{version}
    
'''


def render_module(module, doc='rst', write=False):
    (name, vers) = module['name'], module['version']
    (fname, info) = '', ''
    path = os.path.join('modules', name, vers)
    if not os.path.exists(path):
            os.makedirs(path)
    if doc == 'rst':
        fname = 'index.rst'
        info = rst_template.render(module)
    elif doc == 'yaml':
        fname = 'info.yaml'
        info = yaml.format(**module)
    fpath = os.path.join(path, fname)
    if write:
        with open(fpath, 'w') as file:
            try:
                file.write(info)
            except:
                print "problem writing", file
            finally:
                file.close()
    else:
        line = '*' * len(fpath)
        print line
        print fpath
        print line
        print info

def render(data, versions):
    for name, module in sorted(data.items()):
        for version in versions.get(name, ''):
            module['version'] = version
            module['categories'] = list(module['categories'])
            module['tags'] = list(module['tags'])
            module['compiler'] = 'none specified'
            if '+' in version:
                (v, compiler) = version.split('+', 1)
                module['compiler'] = compiler
            render_module(module, doc='yaml', write=True)

render(data, versions)
