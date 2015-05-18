import struct

VERSION = 0

SEP = chr(31)  # ASCII unit separator


def to_int(bs):
    """Unpack a bytestring as an 4-byte integer"""
    return struct.unpack(">i", bs)[0]


def to_double(bs):
    """Unpack a bytestring as an 8-byte double"""
    return struct.unpack(">d", bs)[0]


def read_int(f):
    """Read a 4-byte big-endian integer from f"""
    return to_int(f.read(4))


def read_double(f):
    """Read a 8-byte big-endian double from f"""
    return to_double(f.read(8))


def materialize(n, indices):
    """Fully materialize a row vector given a row length
    and sequence of [index,value] pairs

    Ex:
        materialize(10, [[2,47], [5,62], [8,94]])
        [0.0 0.0 47 0.0 0.0 62 0.0 0.0 94 0.0]
    """
    row = [0.0] * n
    for idx, val in indices:
        row[idx] = val
    return row


def num_values(row):
    """Count the number of nonzero values in a row"""
    count = 0
    for v in row:
        if v != 0.0:
            count += 1
    return count


def write(fname, labels, rows):
    with open(fname, "wb") as f:
        # Version
        f.write(struct.pack(">i", VERSION))

        # Labels
        label_str = SEP.join([str(l) for l in labels])
        f.write(struct.pack(">i", len(label_str)))
        for char in label_str:
            f.write(struct.pack(">H", ord(char)))

        # Rows
        for row in rows:
            f.write(struct.pack(">i", num_values(row)))
            idx = 0
            for d in row:
                if d != 0.0:
                    f.write(struct.pack(">i", idx))
                    f.write(struct.pack(">d", d))
                idx += 1


class BTable(object):
    def __init__(self, fname):
        self.fname = fname
        self.version = self._version()
        self.labels = self._labels()

    def _read_version(self, f):
        version = read_int(f)
        if version != VERSION:
            raise Exception("Unsupported version: {}".format(version))
        return version

    def _version(self):
        with open(self.fname, "rb") as f:
            return self._read_version(f)

    def _read_labels(self, f):
        """Read an array of labels as a delimited string of 2-byte chars"""
        labels_len = read_int(f)
        labels = [unichr(struct.unpack(">H", f.read(2))[0])
                  for i in range(labels_len)]
        return "".join(labels).split(SEP)

    def _labels(self):
        with open(self.fname, "rb") as f:
            version = self._read_version(f)
            return self._read_labels(f)

    def rows(self):
        """Return a generator that yields dense materialized rows"""
        with open(self.fname, "rb") as f:
            version = self._read_version(f)
            feature_count = len(self._read_labels(f))

            while True:
                bs = f.read(4)
                if bs == '':
                    break
                nvals = to_int(bs)
                indices = [[read_int(f), read_double(f)]
                           for i in range(nvals)]
                yield materialize(feature_count, indices)
