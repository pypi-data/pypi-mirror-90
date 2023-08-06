import io
import codecs
import zipfile
from collections import deque

from .err import NoArchive


__all__ = ('ZipFile',)

class ZipFile:
    DELATED = zipfile.ZIP_DEFLATED
    LZMA = zipfile.ZIP_LZMA
    STORED = zipfile.ZIP_STORED
    BZIP = zipfile.ZIP_BZIP2
    
    def __init__(self, ztype = None, compresslevel = 6):
        if ztype is None:
            ztype = self.DELATED
        self.ztype = ztype
        self.cpl = int(compresslevel)
        self.files = deque()

    def add(self, title, content):
        self.files.append((title, content))
        return len(content)

    def addf(self, fn):
        with codecs.open(fn, 'rb') as f:
            con = f.read()
        self.add(fn, con)

    def get(self, title):
        for t, c in self.files:
            if t == title:
                return c
        else:
            raise NoArchive(f'No Such Archive {title}')

    def list(self):
        return tuple(map(lambda x: x[0], self.files))

    def flush(self, f = None):
        if not f:
            f = io.BytesIO()
        zf = zipfile.ZipFile(f, 'w', self.ztype, True, self.cpl)
        for t, c in self.files:
            zf.writestr(t, c)
        zf.close()
        return f

    def save(self, fn):
        with codecs.open(fn, 'wb') as f:
            return f.write(self.flush().getvalue())

