#!/bin/sh

# Print a sorted list of all loaded modules yesterday 
# with the total number of times they were loaded

DATE=`date --date yesterday "+%Y%m%d"`
BASE="/project/rcc/usageinfo/modulecmd/modulecmd-"
LOG="$BASE$DATE.log"

FILTER='
    { modcount[$4] += $1 }

    END { 
        for (mod in modcount) print mod, modcount[mod]
    }'

awk "$FILTER" $LOG
