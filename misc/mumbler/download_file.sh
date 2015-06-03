#!/bin/bash

echo "Downloading Files from http://storage.googleapis.com/books/ngrams/books/datasetsv2.html..."

echo "Script $0 running on CLI: $HOSTNAME for user: $LOGNAME";
echo "$0 invoked  with Parameters: $@"
echo "$0 invoked with Parameter Count: $#"

if [ $# -lt 2 ]
then
    echo "$0 args: <start> <stop>"
    exit 1
fi

start=${1}
stop=${2}

cnt=$start

while [ $cnt -le $stop ];
do
	echo "Downloading http://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-2gram-20090715-$cnt.csv.zip..."
	cmd="wget --no-check-certificate http://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-2gram-20090715-$cnt.csv.zip"
	echo $cmd
	eval $cmd
	echo "Downloaded http://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-2gram-20090715-$cnt.csv.zip..."
	cnt=$((cnt + 1))
done

exit 0
