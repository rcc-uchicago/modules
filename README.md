# modules

We'd like to ...

* gather basic info for our existing modules
* establish a convention for specifying this info as part of the module build
  process
* use this info to auto-generate our sphinx-based module documentation

The first item is [a nascent student project](https://github.com/rcc-uchicago/docs/blob/master/student-projects/modules.md).

The second item is likely to consist of a [yaml](http://en.wikipedia.org/wiki/YAML) file (see [`info.yaml`](info.yaml)) that gets included in each software package's build folder under `pubsw/software/build`.


## Utilities

Note the two proof-of-concept utility scripts:

* `seed-generator/parse.py` - parses an [inverted-index of
  modules](seed-generator/inverted-index.txt) organized by category and
  generates an `info.yaml` seed files for each of the categorized modules
* `yaml-to-rst/convert.js` - converts a module's `info.yaml` file into
  a restructuredtext format


## Reference

* [rcc module list](http://docs.rcc.uchicago.edu/modulelist.html)
  * [supplemented list](https://github.com/rcc-uchicago/docs/blob/master/software.md) - containing brief descriptions and links
  * [harvard's list](https://rc.fas.harvard.edu/resources/module-list/#)

* [rcc module build process](https://w3.rcc.uchicago.edu/redmine/projects/rcc/wiki/Software_Build_and_Module_Process)
* [build scripts README](https://w3.rcc.uchicago.edu/redmine/projects/pubsw/repository/entry/software/build/README)

* [module system overview](http://www.admin-magazine.com/HPC/Articles/Environment-Modules) - nice article overviewing Environment Modules (the  module system used by the RCC)
