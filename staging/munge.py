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
license: {license}
categories: {categories}
tags: {tags}
url: {url}
usage:
'''


def print_yaml(module):
    (name, vers) = module['name'], module['version']
    fpath = "`{}/{}/info.yaml`".format(name, vers)
    # with open(fpath, 'w') as file:
    print "####", fpath
    print yaml.format(**module)

def print_rst(module):
    rst = rst_template.render(module)
    (name, vers) = module['name'], module['version']
    fpath = "`pubsw/userguide/docs/modules/{}-{}`".format(name, vers)
    line = '*' * len(fpath)
    print line
    print fpath
    print line
    print rst

for name, module in sorted(data.items()):
    for version in versions.get(name, ''):
        module['version'] = version
        module['categories'] = list(module['categories'])
        module['tags'] = list(module['tags'])
        # print_yaml(module)
        print_rst(module)
