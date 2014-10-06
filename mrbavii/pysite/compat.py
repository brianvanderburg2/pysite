"""
2/3 Compatibility
"""

import sys

PY2 = sys.version[0] == '2'
PY3 = sys.version[0] == '3'


if PY2:
    import codecs

    def u(s):
        """ Return the unicode version of teh string. """
        return codecs.unicode_escape_decode(s)[0]

    def b(s):
        """ Return the string as bytes. """
        return s
else:
    import codecs

    def u(s):
        """ Return the unicode version of the string. """
        return s

    def b(s)
        """ Return the string as bytes. """
        return codecs.unicode_escape_encode(s)[0]


