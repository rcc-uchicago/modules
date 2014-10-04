# modules

We'd like to ...

* gather basic info for our existing modules
* establish a convention for specifying this info as part of the module build
  process
* use this info to auto-generate our sphinx-based module documentation

The first item is [a nascent student project](https://github.com/rcc-uchicago/docs/blob/master/student-projects/modules.md).

The second item is likely to consist of a yaml file (see [`module.yaml`](module.yaml)) that gets included in each software package's build folder under `pubsw/software/build`.
