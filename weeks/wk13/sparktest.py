__author__ = 'ssatpati'

#rdd4 = sc.textFile("/Users/ssatpati/tmp/test-dataset.txt")
#rdd5 = rdd4.flatMap(lambda x: x.split(' ')).map(lambda x: (x, 1)).reduceByKey(add).sortByKey(False)

#Another way:

#rdd3 = rdd.map(lambda x: x.split(' ')).flatMap(lambda x: x)
#rdd.map(lambda x: x.split(' ')).flatMap(lambda x: x).take(10)
#rdd.map(lambda x: x.split(' ')).flatMap(lambda x: x).map(lambda x: (x, 1)).reduceByKey(add).take(10)

