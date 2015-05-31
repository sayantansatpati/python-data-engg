#!/usr/bin/python
# Copyright 2009-2010 Yelp
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The classic MapReduce job: count the frequency of words.
"""
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