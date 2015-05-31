__author__ = 'ssatpati'

import urllib
import sys
import locale
import codecs

def set_stdout():
  """
  Set ``sys.stdout`` to the *preffered locale*.

  If called again, set it back to the privious value.

  This is can be used to write UTF-8 encoded content to the console in Python < 3.

  .. note:: The *preffered locale* should be UTF-8 (at least on modern Linux).

  """
    global __stdout
    if __stdout:
        sys.stdout, __stdout = __stdout, None
    else:
        __stdout = sys.stdout
    sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)

QUERY = "#WorldCup #Brazil2014"

print(urllib.quote_plus(QUERY))

print(sys.getdefaultencoding())
print(sys.getfilesystemencoding())
print(locale.getpreferredencoding())

