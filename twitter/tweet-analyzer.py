__author__ = 'ssatpati'

import tweepy
import datetime
import os
import glob
import codecs
import shutil
from nltk import *
from nltk.corpus import stopwords
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import boto

'''Twitter Query'''
QUERY = "microsoft AND mojang"
SINCE = "2015-02-07T00:00:00"
UNTIL = "2015-02-13T00:00:00"
LIMIT_TWEETS = None
PARTITION_HOURS = 24

'''Date & Time Formats used to partition the Data into Files'''
DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
FILE_DATE_TIME_FORMAT = "%Y-%m-%d_%H-%M-%S"

'''Output DIR'''
OUTPUT_DIR = "output"

'''S3 Bucket'''
BUCKET_NAME="assignment2-tweets"


def acquire_store_analyze_tweets():
    """Acquire, Load, & Store Tweets"""
    count = 0
    tokens = []

    # Acquire Tweets & Store in Local Files
    acquire_store_tweets()

    # Move tweets to AWS S3 Bucket
    move_tweets_s3(BUCKET_NAME)

    # Load Tweets from Local
    os.environ["NLTK_DATA"] = "/Users/ssatpati/nltk_data"
    sw = stopwords.words('english')
    tokenizer = RegexpTokenizer(r'\w+')
    for tweet in load_tweets():
        l = [t for t in tokenizer.tokenize(tweet) if t.lower() not in sw]
        tokens.extend(l)
        count += 1

    print(tokens)
    print("[INFO] Total Number of Tweet File Processed: {0}; Total Number of Tokens: {1}".format(count, len(tokens)))

    fdist = FreqDist(tokens)
    print(fdist.items())
    fdist.tabulate(20)  # Show Top 20
    fdist.plot()

    # Clean Up Local Files


def load_tweets():
    """Load Tweets from Local Files"""
    for root, dirnames, filenames in os.walk(OUTPUT_DIR):
        for filename in filenames:
            with codecs.open(OUTPUT_DIR + "/" + filename, 'r', encoding='utf8') as f:
                yield f.read()


def acquire_store_tweets(query=QUERY, since=SINCE, until=UNTIL, partition_hours=PARTITION_HOURS, limit_tweets=None):
    """Acquire Files using Tweepy API"""
    api = get_tweepy_api()

    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
        os.makedirs(OUTPUT_DIR)
    else:
        os.makedirs(OUTPUT_DIR)

    # Convert into DateTime
    since_dt = datetime.datetime.strptime(since, DATE_TIME_FORMAT)
    until_dt = datetime.datetime.strptime(until, DATE_TIME_FORMAT)

    # Counter
    cnt_across = 0

    # Tweets are acquired & stored for every Date Partition, which is configurable
    for t1, t2 in date_partition(since_dt, until_dt, partition_hours):
        cnt = 0
        f_name = "".join(["./",
                          OUTPUT_DIR, "/tweet",
                          "_",
                          t1.strftime(FILE_DATE_TIME_FORMAT),
                          "__",
                          t2.strftime(FILE_DATE_TIME_FORMAT)])

        f = open(f_name, "a")
        print("Output File:{0}".format(f_name))

        for tweet in tweepy.Cursor(api.search,
                                   q=query,
                                   since=t1.strftime(DATE_TIME_FORMAT),
                                   until=t2.strftime(DATE_TIME_FORMAT)).items(limit_tweets):
            #print(tweet)
            f.write(tweet.text.encode('utf-8') + "\n")
            cnt += 1
            cnt_across += 1

        print("~ {0} Tweets Dumped from {1} TO {2}\n".format(cnt, t1, t2))
        f.close()
    print "Total Number of Tweets Acquired: {0}".format(cnt_across)


def date_partition(start, end, partition_hours):
    """Partition Start and End Date by Partition Hours"""
    return datetime_partition(start, end, datetime.timedelta(hours=partition_hours))


def datetime_partition(start, end, duration):
    """Date Time Partition Generator"""
    current = start
    while end > current:
        yield (current + datetime.timedelta(seconds=1), current + duration)
        current = current + duration


def get_tweepy_api():
    """Tweepy API"""
    consumer_key = "";
    consumer_secret = "";

    access_token = "";
    access_token_secret = "";

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    return tweepy.API(auth)


def move_tweets_s3(bucket_name):
    """Move Tweets to S3 Bucket"""
    conn = S3Connection('', '')

    # Delete Bucket contents and Bucket, if one is available
    bucket = None
    try:
        bucket = conn.get_bucket(bucket_name)
        # Delete Files
        print("Deleting Files in S3 Bucket - {0}".format(bucket_name))
        for key in bucket.list():
            key.delete()
        print("Deleting S3 Bucket - {0}".format(bucket_name))
        # Delete Bucket
        conn.delete_bucket(bucket_name)
    except boto.exception.S3ResponseError as err:
        print(err)

    bucket = conn.create_bucket(bucket_name)

    print("Bucket Created in S3 - {0}".format(bucket_name))

    cnt = 0
    for name in glob.glob(OUTPUT_DIR + "/*"):
        print("Copying {0} to S3: {1}".format(name, bucket_name))
        cnt += 1
        k = Key(bucket)
        k.key = name.split("/")[-1]
        k.set_contents_from_filename(name)

    print("{0} Files Copied into S3 Bucket - {1}".format(cnt, bucket_name))


if __name__ == '__main__':
    '''Main Point of Entry to Program'''
    acquire_store_analyze_tweets()
