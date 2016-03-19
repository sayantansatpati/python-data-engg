__author__ = 'ssatpati'

from boto.s3.connection import S3Connection
from boto.s3.key import Key
import boto
import yaml


with open("/Users/ssatpati/.aws/credentials", "r") as f:
    for l in f:
        if l.startswith('aws'):
            t = l.split('=')
            print t[0].strip(),t[1].strip()

conn = S3Connection()

# Delete Bucket contents and Bucket, if one is available
bucket = None
try:
    bucket = conn.get_bucket('w261')

    for i in xrange(3):
        k = Key(bucket)
        k.key = 'hw93/dangling_mass/{0}'.format(i)
        k.set_contents_from_string(str(i))

    for i in xrange(3):
        k = Key(bucket)
        k.key = 'hw93/dangling_mass/{0}'.format(i)
        print k.get_contents_as_string()


except boto.exception.S3ResponseError as err:
    print(err)