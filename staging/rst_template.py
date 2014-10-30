# interpolate in the following string
template = '''
.. index::
  single: {name}

.. _mdoc_{name}:

{header}
{content}
.. _{name}: {url}
'''

def render(name, content, url):
    line = '-' * (len(name) + 1)
    header = "{line}\n{name}_\n{line}".format(line=line, name=name)
    return template.format(name=name, header=header, content=content, url=url)
