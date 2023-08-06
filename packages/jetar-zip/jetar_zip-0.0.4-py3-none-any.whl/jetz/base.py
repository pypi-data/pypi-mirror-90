import io
import codecs
from collections import deque

from .err import NoArchive


__all__ = ('Base',)

class Base:
    def __init__(self):
        self.files = deque()

    def add(self, title, content):
        if title in self.list():
            return self.set(title, content)
        self.files.append((title, content))
        return len(content)

    def addf(self, fn):
        with codecs.open(fn, 'rb') as f:
            con = f.read()
        return self.add(fn, con)

    def get(self, title):
        for t, c in self.files:
            if t == title:
                return c
        else:
            raise NoArchive(f'No Such Archive {title} in')

    def set(self, title, val):
        try:
            p = self.list().index(title)
            self.files[p] = (title, val)
        except:
            self.files.append((title, val))
        return len(val)

    def remove(self, title):
        try:
            p = self.list().index(title)
        except Exception as e:
            raise NoArchive(f'No Such Archive {title} in')
        r = self.files[p]
        self.files.remove(r)
        return r

    def list(self):
        return tuple(map(lambda x: x[0], self.files))

    def add_form_data(self, data):
        fn = data.filename
        b = io.BytesIO()
        data.save(b)
        return self.add(fn, b.getvalue())

    def __iter__(self):
        self._l = self.list()
        self._l.__iter__()
        return self

    def __next__(self):
        return self._l.__next__()
