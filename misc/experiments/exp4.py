__author__ = 'ssatpati'
import numpy as np

arr = np.random.randint(0,10, size=(1, 10))


mean = np.mean(arr)
std = np.std(arr)
summ = np.sum(arr)

print "### Initial Array"
print arr
print mean, std
print summ

arr = arr * 1.0 / summ

mean = np.mean(arr)
std = np.std(arr)
summ = np.sum(arr)

print "### Normalized Array"
print arr
print mean, std
print summ

print "### Noise"
noise = std * np.random.randn(1,10) + mean
print noise
print np.sum(noise)
print np.sum(noise * 1.0 / np.sum(noise))
