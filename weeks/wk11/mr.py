from mrjob.job import MRJob
import re
from sys import stderr

WORD_RE = re.compile(r"[\w']+")
out=stderr

class MRWordFreqCount(MRJob):

    def mapper(self, _, line):
        #for word in re.findall(WORD_RE,line):
        for word in WORD_RE.findall(line):
            out.write('mapper '+word.lower()+'\n')
            yield (word.lower(), 1)

    def combiner(self, word, counts):
        #yield (word, sum(counts))
        c_counts=[c for c in counts]  # extract list from iterator
        total=sum(c_counts)
        out.write('combiner '+word+' ['+','.join([str(c) for c in c_counts])+']='+str(total)+'\n')
        yield (word, total)

    def reducer(self, word, counts):
        #yield (word, sum(counts))
        r_counts=[c for c in counts]  # extract list from iterator
        total=sum(r_counts)
        out.write('reducer '+word+' ['+','.join([str(c) for c in r_counts])+']='+str(total)+'\n')
        yield (word, total)

if __name__ == '__main__':
    MRWordFreqCount.run()
