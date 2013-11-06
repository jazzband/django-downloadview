# -*- coding: utf-8 -*-
"""Low-level IO operations, for use with file wrappers."""
from __future__ import absolute_import
import io


class StringIteratorIO(io.TextIOBase):
    """A dynamically generated StringIO-like object.

    Original code by Matt Joiner <anacrolix@gmail.com> from:

    * http://stackoverflow.com/questions/12593576/adapt-an-iterator-to-behave-like-a-file-like-object-in-python
    * https://gist.github.com/anacrolix/3788413

    """
    def __init__(self, iterator):
        self._iter = iterator
        self._left = ''

    def readable(self):
        return True

    def _read1(self, n=None):
        while not self._left:
            try:
                self._left = next(self._iter)
            except StopIteration:
                break
        ret = self._left[:n]
        self._left = self._left[len(ret):]
        return ret

    def read(self, n=None):
        l = []
        if n is None or n < 0:
            while True:
                m = self._read1()
                if not m:
                    break
                l.append(m)
        else:
            while n > 0:
                m = self._read1(n)
                if not m:
                    break
                n -= len(m)
                l.append(m)
        return ''.join(l)

    def readline(self):
        l = []
        while True:
            i = self._left.find('\n')
            if i == -1:
                l.append(self._left)
                try:
                    self._left = next(self._iter)
                except StopIteration:
                    self._left = ''
                    break
            else:
                l.append(self._left[:i + 1])
                self._left = self._left[i + 1:]
                break
        return ''.join(l)
