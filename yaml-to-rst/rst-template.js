'use strict';

module.exports = function (name, url, content) {

    var header, i, il, line;

    line = [];
    for (i = 0, il = name.length + 1; i < il; ++i) {
        line.push('-');
    }
    line = line.join('');
    header = line + "\n" + name + "_\n" + line;

    return ".. index::\n    single: " +
            name + "\n\n.. _mdoc_" + 
            name + ":\n\n" + 
            header + "\n\n" + 
            content + "\n\n.. _" + 
            name + ": " + 
            url;
};
