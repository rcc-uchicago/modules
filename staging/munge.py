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


# rendering functions follow


def make_cat_idx(name, items):
    entry = '   single: category/{}; {}\n'
    result = ''
    for i in items:
        result += entry.format(i, name)
    return result.rstrip()


def make_tag_idx(name, items):
    entry = '   single: {}; {}\n'
    result = ''
    for i in items:
        result += entry.format(i, name)
    return result.rstrip()


def render_module(module, write=False):
    mod = deepcopy(module)
    name = mod['name']
    line = '-' * (len(name) + 1)
    mod['header'] = "{line}\n{name}_\n{line}".format(line=line, name=name)
    # generate index entries for categories and tags
    mod['cat_idx'] = make_cat_idx(name, mod['categories'])
    mod['tag_idx'] = make_tag_idx(name, mod['tags'])
    info = module_rst.format(**mod)

    if write:
        path = os.path.join('modules', name)
        if not os.path.exists(path):
            os.makedirs(path)
        fpath = os.path.join('modules', name, 'index.rst')
        with open(fpath, 'w') as file:
            try:
                file.write(info)
            except:
                print "problem writing", file
            finally:
                file.close()
    else:
        print '*' * 79
        print info
        print '*' * 79
        print


def render_module_version(module, doc='rst', write=False):
    (fname, info) = '', ''
    if doc == 'rst':
        fname = 'index.rst'
        mod = deepcopy(module)
        (name, vers) = mod['name'], mod['version']
        line = '-' * (len(name) + len(vers) + 1)
        header = "{line}\n{name}/{vers}\n{line}".format(line=line, 
                                                        name=name,
                                                        vers=vers)
        mod['header'] = header
        # convert lists to comma-separated string values
        if not 'usage' in mod:
            mod['usage'] =  '``module load {name}/{version}``'.format(**mod)
        info = module_version_rst.format(**mod)
    elif doc == 'yaml':
        fname = 'info.yaml'
        info = module_version_yaml.format(**module)
    if write:
        (name, vers) = module['name'], module['version']
        path = os.path.join('modules', name, vers)
        if not os.path.exists(path):
                os.makedirs(path)
        fpath = os.path.join(path, fname)
        with open(fpath, 'w') as file:
            try:
                file.write(info)
            except:
                print "problem writing", fpath
            finally:
                file.close()
    else:
        print '~' * 79
        print info


def render_modules(data, versions, write=False):
    for name, module in sorted(data.items()):
        render_module(module, write=write)
        for version in versions.get(name, ''):
            module['version'] = version
            module['compiler'] = 'none specified'
            if '+' in version:
                (v, compiler) = version.split('+', 1)
                module['compiler'] = compiler
            render_module_version(module, doc='rst', write=write)


def render_module_list(modules, categories, write=False):
    content = ''
    for cat in sorted(categories):
        line = '=' * len(cat)
        content += '{line}\n{cat}\n{line}\n\n'.format(line=line, cat=cat)
        for mod in sorted(categories[cat]):
            desc = modules[mod]['description']
            content += '* :ref:`module_{}` - {}\n'.format(mod, desc)
        content += '\n'
    doc = module_list_rst.format(content=content)
    if write:
        fpath = 'modules/index.rst'
        with open(fpath, 'w') as file:
            try:
                file.write(doc)
            except:
                print "problem writing", fpath
            finally:
                file.close()
    else:
        print doc


# render_modules(data, versions, write=False)
render_module_list(data, cats, write=True)
