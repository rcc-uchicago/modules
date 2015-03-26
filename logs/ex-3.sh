#!/bin/sh

# Print a sorted list of all modules with count of unique users 
# who loaded that module yesterday

DATE=`date --date yesterday "+%Y%m%d"`
BASE="/project/rcc/usageinfo/modulecmd/modulecmd-"
LOG="$BASE$DATE.log"

FILTER='
    { modusercount[$4,$3] = 1 } 

    END { 
        for (moduser in modusercount) {
            split(moduser,sep,SUBSEP)
            modcount[sep[1]]++
        } 

        for (mod in modcount) { 
            print mod, modcount[mod]
        }
    }' 

awk "$FILTER" $LOG | sort

