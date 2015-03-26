# Module Logs

We're parsing logs of module loads daily to files located in `/project/rcc/usageinfo/modulecmd/` and have created a back history, e.g.:

    head /project/rcc/usageinfo/modulecmd/modulecmd-20150324.log
        6 midway001 sdjacobs ant/1.8.4
        6 midway001 sdjacobs antlr/2.7
        6 midway001 sdjacobs boost/1.50
        6 midway001 sdjacobs cdo/1.6
        6 midway001 sdjacobs cmake/2.8
        6 midway001 sdjacobs emacs/24
        24 midway001 sdjacobs env/rcc
        6 midway001 sdjacobs git/2.2
        6 midway001 sdjacobs graphviz/2.28
        6 midway001 sdjacobs grib_api/1.9

The last three columns are the machine the module was loaded on (`midway001`), the user who loaded it (`sdjacobs`), and the module. The first column is the number of times that user loaded it on that machine (typically not very useful, since it could be a user's jobs or repeated logging in).

Below are a few potentially useful commands for accessing the data interactively.


#### [`ex-1.sh`](ex-1.sh)

List users who loaded the gcc/4.8 module yesterday:

    MODULE=gcc/4.8
    DATE=`date --date yesterday "+%Y%m%d"`

    BASE="/project/rcc/usageinfo/modulecmd/modulecmd-"
    LOG="$BASE$DATE.log"

    grep $MODULE $LOG \
        | awk '{ users[$3] = 1 } END { for (user in users) print user; }' \
        | sort


#### [`ex-2.sh`](ex-2.sh)

Print a sorted list of all loaded modules yesterday with the total number of times they were loaded:

    FILTER='
      { modcount[$4] += $1 }

      END { 
            for (mod in modcount) print mod, modcount[mod];
      }'

    awk "$FILTER" $LOG


#### [`ex-3.sh`](ex-3.sh)

Print a sorted list of all modules with count of unique users who loaded that module yesterday:

    DATE=`date --date yesterday "+%Y%m%d"`
    BASE="/project/rcc/usageinfo/modulecmd/modulecmd-"
    LOG="$BASE$DATE.log"

    FILTER='
        { modusercount[$4,$3] = 1 } 

        END { 
            for (moduser in modusercount) {
                split(moduser, sep, SUBSEP)
                modcount[sep[1]]++
            } 

            for (mod in modcount) { 
                print mod, modcount[mod]
            }
        }' 

    awk "$FILTER" $LOG | sort


#### [`ex-4.sh`](ex-4.sh)

Using the env/rcc count as a proxy for the total number of users that day we can render a histogram showing the number of users using a module over time.

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


    # iterate over each log file
    for log in $LOGS
        do 
          DATE="$(date --date $(expr match "$log" ".*-\([0-9]*\)\..*") "+%Y-%m-%d")";
          echo -n "$DATE "
          awk "$FILTER_1" $log
        done  | awk -v cols="$COLUMNS" "$FILTER_2"
