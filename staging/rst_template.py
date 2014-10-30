# interpolate in the following string
template = '''
.. index::
  single: {name}

.. _mdoc_{name}:

{header}

name: {name}

description: "{description}"

version: {version}

license: {license}

categories: {categories}

tags: {tags}

url: {url}

.. _{name}: {url}
'''

def render(module):
    name = module['name']
    line = '-' * (len(name) + 1)
    header = "{line}\n{name}_\n{line}".format(line=line, name=name)
    module['header'] = header
    return template.format(**module)
