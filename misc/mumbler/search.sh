#!/bin/bash

echo "Script $0 running on CLI: $HOSTNAME for user: $LOGNAME";
echo "$0 invoked with Parameters: $@"
echo "$0 invoked with Parameter Count: $#"

if [ $# -lt 2 ]
then
    echo "$0 args: <word> <dir>"
    exit 1
fi

dir=$2
word=$1

export LC_ALL=C
FILES=$dir/googlebooks-eng-all-2gram-20090715-*.zip

rm -f $dir/out

ls $FILES | parallel zipgrep ^word {} >> ${dir}/out

#for i in $FILES
#do
# 	echo "Searching for $word in $dir"
#        cmd="zipgrep \"^${word}\" \"$i\" >> ${dir}/out"
#	eval $cmd
#	echo $cmd
#done

exit 0
