#!/bin/sh

# List users who loaded the gcc/4.8 module yesterday

MODULE=gcc/4.8
DATE=`date --date yesterday "+%Y%m%d"`

BASE="/project/rcc/usageinfo/modulecmd/modulecmd-"
LOG="$BASE$DATE.log"

grep $MODULE $LOG \
    | awk '{ users[$3] = 1 } END { for (user in users) print user; }' \
    | sort

