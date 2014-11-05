# rst template for a module
template = '''
.. index::
   single: module; {name}
{cat_idx}
{tag_idx}

.. _module_{name}:

{header}

{description}

Available versions:

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
