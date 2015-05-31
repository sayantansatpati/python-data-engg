import numpy as np
import random

total = 40

def generate():
    #np.random.ranf()
    l = [i for i in xrange(1, total + 1)]
    print(l)

    print(random.randint(1, total))


if __name__ == '__main__':
   generate()