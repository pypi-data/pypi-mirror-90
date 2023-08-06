import io
import codecs
from collections import deque


__all__ = ('Base',)

class Base:
    def __init__(self):
        self.files = deque()

    def add(self, title, content):
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
            raise NoArchive(f'No Such Archive {title}')

    def list(self):
        return tuple(map(lambda x: x[0], self.files))

    def add_form_data(self, data):
        fn = data.filename
        b = io.BytesIO()
        data.save(b)
        return self.add(fn, b.read())
