import io
import codecs
import zipfile
from collections import deque

from .err import NoArchive
from .base import Base


__all__ = ('ZipFile',)

class ZipFile(Base):
    DELATED = zipfile.ZIP_DEFLATED
    LZMA = zipfile.ZIP_LZMA
    STORED = zipfile.ZIP_STORED
    BZIP = zipfile.ZIP_BZIP2
    
    def __init__(self, ztype = None, compresslevel = 6):
        super().__init__()
        if ztype is None:
            ztype = self.DELATED
        self.ztype = ztype
        self.cpl = int(compresslevel)

    def flush(self, f = None):
        if not f:
            f = io.BytesIO()
        zf = zipfile.ZipFile(f, 'w', self.ztype, True, self.cpl)
        for t, c in self.files:
            zf.writestr(t, c)
        zf.close()
        f.seek(0)
        return f

    def save(self, fn):
        with codecs.open(fn, 'wb') as f:
            return f.write(self.flush().getvalue())
