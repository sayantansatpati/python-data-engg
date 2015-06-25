__author__ = 'ssatpati'
import object_storage
import time

USER = "SLOS530867-3:SL530867"
API_KEY = "46a4ba15b984f2bda6ec9132a9b6205d5c618bdb0cc18e74c121ad0e9f2ca059"
container = "container2"

f = "/Users/ssatpati/0-DATASCIENCE/sem-3/scaling/assignments/swift/ngram-1GB.csv"
f_name = "ngram-1GB.csv"

def upload_download():
    sl_storage = object_storage.get_client(USER, API_KEY, datacenter='dal05')

    print(sl_storage.containers())

    # Delete container (if present)
    try:
        sl_storage[container].delete(True)
    except Exception as e:
        print e

    # Create
    sl_storage[container].create()
    print(sl_storage.containers())

    # Upload/Download Files Twice
    for i in xrange(2):
        file_name = f_name + "-" + str(i)
        print "Uploading File: ", file_name
        sl_storage[container][file_name].create()

        s = time.time()
        sl_storage[container][file_name].load_from_filename(f)
        e = time.time()
        print("Time Taken(s): {0}".format(e-s))
        print("Upload Transfer Rate: {0}".format(1024*1024*1024/(e-s)))

        print(sl_storage[container].objects())

        print "Downloading File: ", file_name
        sl_storage[container][file_name].save_to_filename(file_name)


if __name__ == '__main__':
    upload_download()