from collections import defaultdict as dd

entries = dd(lambda: dd(list))
lines = [x.rstrip().split(':') for x in open('inverted-index.txt')]

for (labels, modules) in lines:
    (cats, tags) = labels.split('|')
    cats = cats.split(',')
    tags = tags.split(',')
    modules = modules.split(',')
    for m in modules:
        entries[m]['tags'].extend(tags)
        entries[m]['cats'].extend(cats)

def pprint():
    for module in entries:
        print "module:", module
        print "tags:", entries[module]['tags']
        print "category:", entries[module]['cats']
        print

def make_yamls():
    pass # generate yaml files

pprint()
