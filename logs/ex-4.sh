#!/bin/sh

# Using the env/rcc count as a proxy for the total number of 
# users that day we can render a histogram showing the number of 
# users using a module over time

LOGS=/project/rcc/usageinfo/modulecmd/modulecmd-*.log

FILTER_1='{ if ($4=="env/rcc") { user[$3] = 1 } } END { print length(user) }' 

FILTER_2='
   BEGIN { max=0; i=0 }

   { 
       day[i]=$1
       count[i] = $2
       i++
       if ($2 > max) max=$2
    } 
   
    END {
        if (max < cols){
            rate=1
        } else { 
            rate = int(max/cols)+1
        } 
        
        for (i=0; i < length(count); i++) { 
            r=""
            j=count[i]/rate
            while (j-->0) r=r"#"
            printf "%s %4u %s\n", day[i], count[i], r
        } 
        
        if (rate>1) { 
            print "where each # = ", rate
        } else {
            print rate
        }
    }'


for log in $LOGS
    do 
      DATE="$(date --date $(expr match "$log" ".*-\([0-9]*\)\..*") "+%Y-%m-%d")";
      echo -n "$DATE "
      awk "$FILTER_1" $log
    done  | awk -v cols="$COLUMNS" "$FILTER_2"
