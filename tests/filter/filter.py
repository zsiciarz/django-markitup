from __future__ import unicode_literals


def testfilter(s, arg=None):
    return s.replace('replace this', arg)


def testfilter_upper(s, skip=None):
    if skip is None:
        skip = []
    return ''.join(ch.upper() if ch not in skip else ch for ch in s)
