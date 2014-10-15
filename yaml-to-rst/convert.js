#!/usr/bin/env node 
'use strict';

var path = process.argv[2],
    fs = require('fs'),
    yaml = require('js-yaml'),
    render = require('rst-template');


if (!path) {
    throw new Error('provide path to yaml file');
}


var convert = function (err, file) {

    var key, rst,
        data = yaml.load(file.toString()),
        content = '';

    for (key in data) {
        content += [key, ': ', data[key], '\n\n'].join('');
    }
    rst = render(data.name, data.url, content);
    console.log(rst);
};


fs.readFile(path, convert);
