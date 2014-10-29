import json

data = dict()

def module(name, url, desc, license):
    return dict(name=name, url=url, description=desc, license=license)

modules = [module(*line.rstrip().split('\t')) for line in open('data.tsv')]

for m in modules: 
    for key in 'version buildpath usage'.split(' '): 
        m[key] = ''
    m['tags'] = []
    m['categories'] = []
    data[m['name']] = m

for row in open('categories.tsv'):
    (cat, modules) = row.rstrip().split('\t')
    for m in modules.split(', '):
        try:
            data[m]['categories'].append(cat)
        except KeyError:
            print m, "<<<<<<<<"

for row in open('cat-tagging.tsv'):
    (tags, modules) = row.rstrip().split('\t')
    for tag in tags.split(', '):
        for module in modules.split(', '):
            try:
                data[m]['tags'].append(tag)
            except KeyError:
                print m, "<<<<<<<<"

for row in open('tags.tsv'):
    (tag, modules) = row.rstrip().split('\t')
    for module in modules.split(', '):
        try:
            data[m]['tags'].append(tag)
        except KeyError:
            print m, "<<<<<<<<"


template = '''
name: {}
description: "{}"
version:  
buildpath: {}/
license: {}
categories: {}
tags: {}
url: {}
usage:
'''

for name, m in data.items():
    print name, template.format(m['name'], 
                                m['description'], 
                                m['name'],
                                m['license'],
                                m['categories'],
                                m['tags'],
                                m['url'])

