#!/bin/bash

echo "Script $0 running on CLI: $HOSTNAME for user: $LOGNAME";
echo "$0 invoked with Parameters: $@"
echo "$0 invoked with Parameter Count: $#"

if [ $# -lt 1 ]
then
    echo "$0 args: <word> <count>"
    exit 1
fi


word=$1
count=$2

cnt=0

s="$(date +%s)"

ROOT="/gpfs/gpfsfpo/ngrams"
aggregate_file="$ROOT/agg"

declare -a words=($word)


until [  "$cnt" -ge "$count" ]; do
	echo -e "@@@ Mumbler Running for Word: $word \n\n"
	echo "@@@ Processing in gpfs1 (Local)"
	cmd="./search.sh $word $ROOT/gpfs1"
	echo $cmd
	eval $cmd &

	pid1=$!

	echo "@@@ Processing in gpfs2 (Remote)"
	cmd="ssh -i ~/.ssh/id_rsa root@gpfs2 'bash -s' < ./search.sh $word $ROOT/gpfs2"
	echo $cmd
	eval $cmd &

	pid2=$!

	echo "@@@ Processing in gpfs3 (Remote)"
	cmd="ssh -i ~/.ssh/id_rsa root@gpfs3 'bash -s' < ./search.sh $word $ROOT/gpfs3"
	echo $cmd
	eval $cmd &

	pid3=$!

	echo "[INFO] Waiting for PID(s): $pid1 $pid2 $pid3"

	wait $pid1
	wait $pid2
	wait $pid3
	
	echo "@@@ Output Files"
	ls -lh $ROOT/*/out
	ls -l $aggregate_file
	rm $aggregate_file

	# Producing Final Output
	cat $ROOT/gpfs*/out | awk -F'[:]' '{print $2}' | awk -F'[" "\t]' '{array[$1"\t"$2]+=$4} END { for (i in array) {print i"\t" array[i]}}' | sort >> $aggregate_file
	
	word=$(head -n $(( ( RANDOM % $(cat $aggregate_file | wc -l) )  + 1 )) $aggregate_file | tail -1 | cut -f2)
	cnt=$(( cnt + 1 ))
	words+=($word)

	e="$(date +%s)"
	echo "[INFO] $(date) Time Taken(s) so far: $((e-s))"
done

e="$(date +%s)"
echo "[INFO] $(date) Total Time Taken(s): $((e-s))"

echo "--------------------------------"
echo "--------------------------------"
echo "~~~~~~~~~~~ MUMBLER ~~~~~~~~~~~~"
echo ${words[@]}
echo "--------------------------------"
echo "--------------------------------"





