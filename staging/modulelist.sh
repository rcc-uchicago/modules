#!/bin/sh

SRCDIR="$(dirname "$(readlink -f ${BASH_SOURCE[0]})")"
swdocdir=$SRCDIR/docs/software

echo "

.. _software_module_list:

=====================================================================
Software Module List
=====================================================================

This is an auto-generated list of software modules available on Midway.

Run \`\`module load <modulename>\`\` to load any of these modules in to your
environment.  For more information on using software modules see :ref:\`intro-to-software-modules\`


"

echo "

.. csv-table::
   :header: "Application", "Module Name", "Version", "Compiler"
   :widths: 20, 40, 20, 30
"

IFS='
'
lastmodule=''
for module in `module avail  -t 2>&1 |grep -v -- ^- | sort`; do

   default=N
   bold=''

   if [[ $module =~ "(default)" ]]; then
       default=Y
       bold='**'
       module="${module%   (default)}"
   fi
   
   appname=${module%/*}
   appver=${module#*/}
   compiler=' '
   if [[ $appver =~ "+" ]]; then
       compiler=${appver#*+}
       appver=${appver%%+*}
   fi

   if grep -qr "^.. _mdoc_$appname:$" $swdocdir; then
       appname=":ref:\`$appname <mdoc_$appname>\`"
   fi

   if [ "$lastmodule" != "$appname" ]; then
       printname=$appname
   else
       printname=""
   fi
   lastmodule=$appname

   # this check eliminates stuff like use.own
   if [ $appname != $appver ]; then
       echo "   $printname",":doc:\`${module} <modules/${module}/index>\`","$appver","$compiler"
   fi

done
