# yaml template for a versioned module
template = '''
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


