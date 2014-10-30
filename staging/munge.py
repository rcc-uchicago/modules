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


template = '''
name: {}
description: "{}"
version: {}
license: {}
categories: {}
tags: {}
url: {}
usage:
'''

for name, m in sorted(data.items()):
    for version in versions.get(name, ''):
        fpath = "`{}/{}/info.yaml`".format(name, version)
        yaml = template.format(m['name'], 
                                    m['description'], 
                                    version,
                                    m['license'],
                                    list(m['categories']),
                                    list(m['tags']),
                                    m['url'])
        # with open(fpath, 'w') as file:
        print "####", fpath
        print yaml

