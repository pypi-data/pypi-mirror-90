import io
import codecs
import tarfile
from collections import deque

from .err import NoArchive
from .base import Base

__all__ = ('TarFile',)

class TarFile(Base):
    STORED = 0
    GZIP = 1
    BZIP = 2
    LZMA = 3
    FMT_USTAR = tarfile.USTAR_FORMAT
    FMT_GNU = tarfile.GNU_FORMAT
    FMT_PAX = tarfile.PAX_FORMAT
    
    def __init__(self, ttype = None, tfmt = None):
        super().__init__()
        if ttype is None:
            ztype = self.BZIP
        self.ttype = ttype
        self.tfmt = tfmt

    def flush(self, f = None, name = None):
        t = self.ttype
        if t == 0:
            oft = 'w'
        elif t == 1:
            oft = 'w:gz'
        elif t == 2:
            oft = "w:bz2"
        else:
            oft = "w:xz"
        if not f:
            f = io.BytesIO()
        zf = tarfile.open(name, oft, f, format = self.tfmt)
        ti = tarfile.TarInfo
        for t, c in self.files:
            zf.addfile(ti(t), c)
        zf.close()
        f.seek(0)
        return f

    def save(self, fn):
        with codecs.open(fn, 'wb') as f:
            return f.write(self.flush().getvalue())
