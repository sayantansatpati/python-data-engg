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
import os
import sys
import codecs
import locale

WORD_RE = re.compile(r"[\w']+")
sys.stderr = codecs.getwriter(locale.getpreferredencoding())(sys.stderr)
out = sys.stderr

class MRWordFreqCount(MRJob):

    def mapper(self, _, line):
         #for word in re.findall(WORD_RE,line):
        filename = os.environ['map_input_file']
        #out.write(filename)
        #line = line.decode(sys.getdefaultencoding()).encode('utf-8')
        try:
            out.write("[" + line + "]\n")
            for word in WORD_RE.findall(line):
                #out.write('mapper '+ word + "\t" + filename + '\n')
                out.write(word + " [M] " + filename + "\n")
                yield (word, filename)
        except:
            e = sys.exc_info()[0]
            pass

    def combiner(self, word, documents):
        #yield (word, sum(counts))
        #c_counts=[c for c in counts]  # extract list from iterator
        #total=sum(c_counts)
        #out.write('combiner '+word+' ['+','.join([str(c) for c in c_counts])+']='+str(total)+'\n')
        #yield (word, total)
        try:
            out.write(word + " [C] " + "D1" + '\n')
            yield (word, documents[0])
        except:
            e = sys.exc_info()[0]
            pass


    def reducer(self, word, documents):
        #yield (word, sum(counts))
        #r_counts=[c for c in counts]  # extract list from iterator
        #total=sum(r_counts)
        #out.write('reducer '+word+' ['+','.join([str(c) for c in r_counts])+']='+str(total)+'\n')
        try:
            out.write(word + " [R] " + " ".join(documents) + '\n')
            yield (word, documents)
        except:
            e = sys.exc_info()[0]
            pass


if __name__ == '__main__':
    MRWordFreqCount.run()