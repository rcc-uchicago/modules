from copy import deepcopy

# interpolate in the following string
template = '''
.. index:: 
   single: {name}; {version}
   single: module; {name}/{version}

{header}

name
    {name}

version
    {version}

description
    {description}

compiler
    {compiler}

license
    {license}

url
    {url}

usage 
    {usage}


.. seealso::

    :ref:`module_{name}`
        List of all available versions of this module.

    :ref:`software_module_list`
        Full list of available software modules available on Midway.

    `Using Software Modules <../../index.html#using-software-modules>`_
        Section of the RCC user guide with additional info on using 
        the module system.

'''

def render(module):
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
    return template.format(**mod)
