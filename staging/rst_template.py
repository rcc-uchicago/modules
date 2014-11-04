from copy import deepcopy

# interpolate in the following string
template = '''
.. index:: {name}/{version}, module, {categories}, {tags}

{header}

name
    {name}

description
    {description}

version
    {version}

compiler
    {compiler}

license
    {license}

categories
    {categories}

tags
    {tags}

url
    {url}

usage 
    {usage}


.. _{name}: {url}
'''

def render(mod):
    module = deepcopy(mod)
    name = module['name']
    line = '-' * (len(name) + 1)
    header = "{line}\n{name}_\n{line}".format(line=line, name=name)
    module['header'] = header
    module['categories'] = ", ".join(module['categories'])
    module['tags'] = ", ".join(module['tags'])
    if not 'usage' in module:
        module['usage'] =  '``module load {name}/{version}``'.format(**module)
    return template.format(**module)
