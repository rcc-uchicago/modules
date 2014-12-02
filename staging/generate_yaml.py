import os
from glob import glob
import subprocess
import pwd
import datetime
from templates import *

SOFTPATH=os.environ['SOFTPATH']

def module_info(module):
    softname = os.path.basename(os.path.dirname(module))
    modulevers = os.path.basename(module)

    if "+" in modulevers:
        softvers, compiler = modulevers.split('+', 1)
    else:
        softvers = modulevers
        compiler = ""

    # evaluate suffix from module file
    cmd = "eval echo `sed -n -e 's/^set\s*suffix\s*\(.*\)$/\\1/p' "+ module + "`"
    suffix = subprocess.check_output(cmd, shell=True).rstrip()
    if suffix:
        directory = SOFTPATH+"/"+softname+"-"+softvers+"-"+suffix
        if compiler:
            directory += "+"+compiler
    else:
        # try evaluating appdir instead
        cmd = "eval echo `sed -n -e 's/^set\s*appdir\s*\(.*\)$/\\1/p' "+ module + "`"
        directory = subprocess.check_output(cmd, shell=True).rstrip()
 
    if os.path.isdir(directory):
        # identify maintainer from directory
        uid = os.stat(directory).st_uid
        try:
            maintainer = pwd.getpwuid(uid).pw_name
            if maintainer == "root":
                maintainer = "wettstein"
        except Exception:
            maintainer = {1832378456:"dylanhall", 57917:"jheddon", 2099035613:"labello"}[uid]

        buildlog = glob(directory+"/build.log-*")
        if buildlog:
            builddate = datetime.datetime.strptime(buildlog[-1].rsplit("-")[-1][0:8],"%Y%m%d").date().isoformat()
        else:
            builddate = ""
    else:
        builddate = maintainer = directory = ""

    if compiler:
        compiler = compiler.replace("-", "/", 1) 
 
    # identify conflicting modules
    cmd = "sed -n -e 's/^conflict //p' " + module
    conflicts = subprocess.check_output(cmd, shell=True)
    conflicts = conflicts.split()
    try:
        conflicts.remove('"$mname"')
    except:
        pass
    try:
        conflicts.remove(softname)
    except:
        pass
    conflicts = ",".join(conflicts)
 
    # parse dependencies from module load command
    cmd = "sed -n -e 's/^module load //p' " + module
    dependencies = subprocess.check_output(cmd, shell=True)
    dependencies = ",".join(dependencies.split())

    return dict(name=softname,version=softvers,compiler=compiler,conflicts=conflicts,
                dependencies=dependencies,maintainer=maintainer,builddate=builddate)

data = {}
for line in open('data.tsv'):
    cols = line.rstrip().split('\t')
    if len(cols) == 4:
        modulename,url,description,license = cols
        name = modulename
    else:
        modulename,name,url,description,license = cols
    data[modulename] = dict(name=name, url=url, description=description, license=license, categories=set(), tags=set())

for row in open('categories.tsv'):
    (cat, modules) = row.rstrip().split('\t')
    for m in modules.split(', '):
        try:
            data[m]['categories'].add(cat)
        except KeyError:
            print m, "<<<<<<<< CAT"

#for row in open('cat-tagging.tsv'):
#    (tags, modules) = row.rstrip().split('\t')
#    for tag in tags.split(', '):
#        for m in modules.split(', '):
#            try:
#                data[m]['tags'].add(tag)
#            except KeyError:
#                print m, "<<<<<<<< CAT-TAG"

for row in open('tags.tsv'):
    (tag, modules) = row.rstrip().split('\t')
    for m in modules.split(', '):
        try:
            data[m]['tags'].add(tag)
        except KeyError:
            print m, "<<<<<<<< TAG"


for m in data:
    if len(data[m]['categories']) == 0:
        print m, data[m]['categories']

    if len(data[m]['tags']) == 0:
        print m, data[m]['categories'], 'no tags'

    data[m]['tags'] = ",".join(data[m]['tags'])
    data[m]['categories'] = ",".join(data[m]['categories'])

moduledir="../modulefiles"
for module in glob(moduledir+"/*/*"):
    if "yaml" in module: continue
    softname = os.path.basename(os.path.dirname(module))
    modulevers = os.path.basename(module)

    minfo = module_info(module)
    modulename = minfo["name"]
    del minfo["name"]
    data[modulename].update(minfo)

    try:
        os.mkdir(moduledir+"/"+modulename)
    except OSError:
        pass

    with open(moduledir+"/"+softname+"/"+modulevers+".yaml","w") as yml:
        print >>yml, module_version_yaml.format(**data[modulename])
