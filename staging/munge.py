import os
import rst_template
from copy import deepcopy

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


rst = '''
.. index::
   single: module; {name}
{cat_idx}
{tag_idx}

.. _module_{name}:

{header}

.. toctree::
   :glob:

   */index

.. seealso::

    :ref:`software_module_list`
        Full list of available software modules available on Midway.

    `Using Software Modules <../../index.html#using-software-modules>`_
        Section of the RCC user guide with additional info on using 
        the module system.

.. _{name}: {url}
'''


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
    info = rst.format(**mod)

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
        info = rst_template.render(module)
    elif doc == 'yaml':
        fname = 'info.yaml'
        info = yaml.format(**module)
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
                print "problem writing", file
            finally:
                file.close()
    else:
        print '~' * 79
        print info


def render(data, versions):
    for name, module in sorted(data.items()):
        render_module(module, write=True)
        for version in versions.get(name, ''):
            module['version'] = version
            module['compiler'] = 'none specified'
            if '+' in version:
                (v, compiler) = version.split('+', 1)
                module['compiler'] = compiler
            render_module_version(module, doc='rst', write=True)


render(data, versions)
