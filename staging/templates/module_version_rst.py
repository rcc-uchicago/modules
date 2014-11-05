# rst template for a versioned module
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
