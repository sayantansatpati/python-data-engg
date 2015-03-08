# Report


**Solution has been implemented using Hadoop Streaming (Python)** 

**Approach Taken:**

1. Mapper side join is done by loading the smaller data set (Artist Band Master List) into each mapper (Distributed Cache).
2. The Artist name is normalized by doing tokenization, stop word removal, and stemming using Python NLTK
3. Similar is done for each Artist Name from the Performance Data Set. Any mismatch is dropped by the Mapper
4. Mapper emits records as <Normalized Artist Name>^<DATE:YYYY-MM-DD)^<Artist Name>^<Performance>.
5. Record from Mapper: ('beatl',)^2013-03-06^The Beatles^1
7. The entire record is treated as a key so everything is sorted when it arrives at the Reducer
8. Other possible approach could have been to treat ('beatl',)^2013-03-06 as the key and rest as value. This approach would 
have sorted only the Normalized Artist Name and Date, but would have generated more data and IO between Mappers and Reducers 
9. Partitioning is done only on the first token (Normalized Artist Name) ensuring 1) better distribution of keys
based only on normalized Artist Name and 2) All records for same Artist end up in same reducer 
10. Reducer Aggregates the Total Performances for each <Normalized Artist Name>^<DATE:YYYY-MM-DD) combination

## NLTK

**Normalization of Artist/Band Name does the following:**

1. Each Artist name is first tokenized by removing the white spaces and other special characters (-, & etc).
2. Stop words are removed ('A', 'The', 'and' etc). NLTK corpora has an exhaustive list of stopwords.
3. Each word is then stemmed, or reduced to its Base/Root Form using the LancasterStemmer
4. Tokens are then sorted for final apple to apple comparison between Master List and Performance Data


- Mapper File: mapper.py
- Reducer File: reducer.py
- Master List of Artist/Bands: artist_band.txt
- Performance of Artist/Bands per Date: performance.txt
    - A few more records have been added over what was provided for covering other scenarios


### Files

    [cloudera@localhost assignment]$ ls -l
    total 20
    -rw-rw-r-- 1 cloudera cloudera  110 Mar  7 22:56 artist_band.txt
    -rwxrwxr-x 1 cloudera cloudera 1781 Mar  7 22:56 mapper.py
    -rw-rw-r-- 1 cloudera cloudera  447 Mar  7 22:56 performance.txt
    -rwxrwxr-x 1 cloudera cloudera 1341 Mar  7 22:56 reducer.py
    

###  artist_band.txt

    The Doors
    Led Zeppelin
    Stevie Wonder
    The Beatles
    Ben Harper
    Ben Harper & The Innocent Criminals
    Foo Fighters


### performance.txt

    Doors, The	1362620749	50
    Led Zeppelin	1362620750	12
    Stevie Wonder	1362620749	5
    Wonder, Stevie	1428439983	10
    Beatles	1362620750	1
    The Beatles	1362620750	250
    The Beatle 	1428439983  	25
    Ben Harper	1362620749	3
    Ben Harper & The Innocent Criminals	1362620749	10
    Ben Harper and the Innocent Criminals	1362620749	1
    Ben Harper; the Innocent Criminals	1428439983	7
    The Foo Fighters	1362620749	1
    Foo Bar Fighters	1362620749	1
    Bar Foo Fighters	1362620749	1


## Testing in local:



### Output from Mapper


    [cloudera@localhost assignment]$ cat performance.txt | python mapper.py | sort -k 1
    ('beatl',)^2013-03-06^The Beatles^1
    ('beatl',)^2013-03-06^The Beatles^250
    ('beatl',)^2015-04-07^The Beatles^25
    ('ben', 'crimin', 'harp', 'innoc')^2013-03-06^Ben Harper & The Innocent Criminals^1
    ('ben', 'crimin', 'harp', 'innoc')^2013-03-06^Ben Harper & The Innocent Criminals^10
    ('ben', 'crimin', 'harp', 'innoc')^2015-04-07^Ben Harper & The Innocent Criminals^7
    ('ben', 'harp')^2013-03-06^Ben Harper^3
    ('door',)^2013-03-06^The Doors^50
    ('fight', 'foo')^2013-03-06^Foo Fighters^1
    ('led', 'zeppelin')^2013-03-06^Led Zeppelin^12
    (u'stevy', 'wond')^2013-03-06^Stevie Wonder^5
    (u'stevy', 'wond')^2015-04-07^Stevie Wonder^10

### Output from Reducer


    [cloudera@localhost assignment]$ cat performance.txt | python mapper.py | sort -k 1 | python reducer.py 
    The Beatles	2013-03-06	251
    The Beatles	2015-04-07	25
    Ben Harper & The Innocent Criminals	2013-03-06	11
    Ben Harper & The Innocent Criminals	2015-04-07	7
    Ben Harper	2013-03-06	3
    The Doors	2013-03-06	50
    Foo Fighters	2013-03-06	1
    Led Zeppelin	2013-03-06	12
    Stevie Wonder	2013-03-06	5
    Stevie Wonder	2016-04-07	10


## Testing in Hadoop Cluster (Cloudera CDH4.7 VirtualBox VM):


### 3 Reducers

#### Hadoop Streaming Command

    hadoop fs -rm -r -skipTrash /user/cloudera/assignment1/output;
    hadoop jar /usr/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.0.0-mr1-cdh4.7.0.jar
    -D stream.map.output.field.separator=^
    -D stream.num.map.output.key.fields=4
    -D map.output.key.field.separator=^
    -D mapred.text.key.partitioner.options=-k1,1
    -D mapred.reduce.tasks=3
    -input /user/cloudera/assignment1/input/performance.txt
    -output /user/cloudera/assignment1/output
    -mapper 'mapper.py' -reducer 'reducer.py'
    -file ./mapper.py -file ./reducer.py
    -file ./artist_band.txt
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner


#### Options

1. stream.map.output.field.separator=^ # Indicates Mapper Delimeter is ^
2. stream.num.map.output.key.fields=4  # Indicates up to 4th ^ is treated as Key
3. map.output.key.field.separator=^    # Indicates Separator for Partition
4.  mapred.text.key.partitioner.options=-k1,1 # Indicates Partition would be done using the 1st field only


#### Output in HDFS

    [cloudera@localhost assignment]$ hadoop fs -ls /user/cloudera/assignment1/output
    Found 5 items
    -rw-r--r--   3 cloudera cloudera          0 2015-03-08 09:53 /user/cloudera/assignment1/output/_SUCCESS
    drwxr-xr-x   - cloudera cloudera          0 2015-03-08 09:53 /user/cloudera/assignment1/output/_logs
    -rw-r--r--   3 cloudera cloudera        200 2015-03-08 09:53 /user/cloudera/assignment1/output/part-00000
    -rw-r--r--   3 cloudera cloudera         55 2015-03-08 09:53 /user/cloudera/assignment1/output/part-00001
    -rw-r--r--   3 cloudera cloudera         53 2015-03-08 09:53 /user/cloudera/assignment1/output/part-00002

#### Contents of Each File

    [cloudera@localhost assignment]$ hadoop fs -cat /user/cloudera/assignment1/output/part-00000
    Ben Harper & The Innocent Criminals	2013-03-06	11
    Ben Harper & The Innocent Criminals	2015-04-07	7
    Ben Harper	2013-03-06	3
    The Doors	2013-03-06	50
    Foo Fighters	2013-03-06	1
    Led Zeppelin	2013-03-06	12
    [cloudera@localhost assignment]$ hadoop fs -cat /user/cloudera/assignment1/output/part-00001
    Stevie Wonder	2013-03-06	5
    Stevie Wonder	2015-04-07	10
    [cloudera@localhost assignment]$ hadoop fs -cat /user/cloudera/assignment1/output/part-00002
    The Beatles	2013-03-06	251
    The Beatles	2015-04-07	25

### 1 Reducer (No Partitioning Required)


#### Hadoop Streaming Command

    hadoop fs -rm -r -skipTrash /user/cloudera/assignment1/output;
    hadoop jar /usr/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.0.0-mr1-cdh4.7.0.jar
    -D stream.map.output.field.separator=^
    -D stream.num.map.output.key.fields=4
    -D mapred.reduce.tasks=1
    -input /user/cloudera/assignment1/input/performance.txt
    -output /user/cloudera/assignment1/output
    -mapper 'mapper.py'
    -reducer 'reducer.py'
    -file ./mapper.py
    -file ./reducer.py
    -file ./artist_band.txt

#### Contents of File

    [cloudera@localhost assignment]$ hadoop fs -cat /user/cloudera/assignment1/output/part-00000
    The Beatles	2013-03-06	251
    The Beatles	2015-04-07	25
    Ben Harper & The Innocent Criminals	2013-03-06	11
    Ben Harper & The Innocent Criminals	2015-04-07	7
    Ben Harper	2013-03-06	3
    The Doors	2013-03-06	50
    Foo Fighters	2013-03-06	1
    Led Zeppelin	2013-03-06	12
    Stevie Wonder	2013-03-06	5
    Stevie Wonder	2015-04-07	10
