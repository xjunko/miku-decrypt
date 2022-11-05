import struct


class BinaryDeserialize:
    def __init__(self, data: bytes):
        self.data = data
        self.i = 0

    def process(self) -> int | dict | list | str | float | bool:
        if self.i >= len(self.data):
            return None

        c = self.data[self.i]

        if 0x00 <= c < 0x80:
            self.i += 1
            return c

        if 0x80 <= c < 0x90:
            self.i += 1
            return self._dict(c - 0x80)

        if 0x90 <= c < 0xA0:
            self.i += 1
            return self._list(c - 0x90)

        if 0xA0 <= c < 0xC0:
            self.i += 1
            return self._str(c - 0xA0)

        if c == 0xC0:
            self.i += 1
            return None

        if c == 0xC2:
            self.i += 1
            return False

        if c == 0xC3:
            self.i += 1
            return True

        if c == 0xCA:
            self.i += 1
            return self._float()

        if c == 0xCC:
            self.i += 1
            return self._uint(1)

        if c == 0xCD:
            self.i += 1
            return self._uint(2)

        if c == 0xCE:
            self.i += 1
            return self._uint(4)

        if c == 0xCF:
            self.i += 1
            return self._uint(8)

        if c == 0xD9:
            self.i += 1
            return self._str(self._uint(1))

        if c == 0xDA:
            self.i += 1
            return self._str(self._uint(2))

        if c == 0xDC:
            self.i += 1
            return self._list(self._uint(2))

        if c == 0xDE:
            self.i += 1
            return self._dict(self._uint(2))

        raise NotImplementedError(c)

    def _dict(self, size):
        s = self._list(size * 2)
        return {key: value for key, value in zip(s[0::2], s[1::2])}

    def _list(self, size):
        return [self.process() for _ in range(size)]

    def _str(self, size):
        s = self.data[self.i : self.i + size].decode()
        self.i += size
        return s

    def _int(self, size):
        s = self.data[self.i : self.i + size]
        self.i += size

        if size == 1:
            return struct.unpack(">b", s)[0]
        if size == 2:
            return struct.unpack(">h", s)[0]
        if size == 4:
            return struct.unpack(">l", s)[0]
        if size == 8:
            return struct.unpack(">q", s)[0]

        raise NotImplementedError()

    def _uint(self, size):
        s = self.data[self.i : self.i + size]
        self.i += size

        if size == 1:
            return struct.unpack(">B", s)[0]
        if size == 2:
            return struct.unpack(">H", s)[0]
        if size == 4:
            return struct.unpack(">L", s)[0]
        if size == 8:
            return struct.unpack(">Q", s)[0]

        raise NotImplementedError()

    def _float(self, size=4):
        s = self.data[self.i : self.i + size]
        self.i += size

        if size == 4:
            return float("%g" % struct.unpack(">f", s)[0])
        if size == 8:
            return struct.unpack(">d", s)[0]

        raise NotImplementedError()
