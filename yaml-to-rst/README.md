# convert

Quick proof-of-concept demonstrating how we can convert a module's `info.yaml` file into restructuredText format for the RCC's sphinx-based docs.

    convert.js input.yaml > output.rst

See [`input.yaml`](input.yaml) and [`output.rst`](output.rst) for sample
input/output.


## rst-template

The `convert.js` script relies on a template function defined in [`rst-template.js`](rst-template.js).  This is where the output template is defined.  It currently takes three strings as arguments: `name`, `url`, and `content`.  (We can easily update the layout of the restructuredText and pass along different or additional parameters.)

Example usage:

```javascript
var render = require('rst-template'),
    name = 'MODULE',
    url = 'http://module.com',
    content = 'MODULE DOCS HERE';

console.log(render(name, url, content));
```

Given the current template layout, this prints ...

    .. index::
        single: MODULE

    .. _mdoc_MODULE:

    -------
    MODULE_
    -------

    MODULE DOCS HERE

    .. _MODULE: http://module.com
