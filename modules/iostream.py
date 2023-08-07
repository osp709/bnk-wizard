"""
iostream Module
"""

import struct


class Stream:
    """
    Stream Class : Stream superclass
    """

    def __init__(self, file: str, fmt: str, little_endian: bool = True):
        if fmt == "rb":
            self.file = open(file, "rb")
        elif fmt == "wb":
            self.file = open(file, "wb")
        else:
            raise OSError("Wrong file read format!")
        self.little_endian = little_endian

    def fmt_str(self, f_str: str):
        """
        Return the struct format string based on little/big endian
        """
        return "<" + f_str if self.little_endian else ">" + f_str

    def get_position(self) -> int:
        """
        Get current location of the file cursor
        """
        return self.file.tell()

    def set_position(self, pos: int) -> None:
        """
        Get file cursor location
        """
        self.file.seek(pos)

    def close(self) -> None:
        """
        Close the file
        """
        self.file.close()


class InputStream(Stream):
    """
    InputStream Class : For endian-based binary input
    """

    def __init__(self, file: str, little_endian: bool = True) -> None:
        super().__init__(file, "rb", little_endian)

    def read_bytes(self, size: int) -> bytes:
        """
        Read data from file as binary
        """
        data = self.file.read(size)
        return data

    def read_str(self, size: int) -> str:
        """
        Read data from file as string
        """
        data = self.file.read(size)
        data = struct.unpack(self.fmt_str(str(size) + "s"), data)
        return data[0].decode()

    def read_int(self) -> int:
        """
        Read data from file as integer
        """
        data = self.file.read(4)
        data = struct.unpack(self.fmt_str("I"), data)
        return data[0]


class OutputStream(Stream):
    """
    OutputStream Class : For endian-based binary output
    """

    def __init__(self, file: str, little_endian: bool = True) -> None:
        super().__init__(file, "wb", little_endian)

    def write_bytes(self, data: bytes) -> int:
        """
        Write binary data to file
        """
        return self.file.write(data)

    def write_str(self, data: str) -> int:
        """
        Write string data to file
        """
        data = struct.pack(self.fmt_str(str(len(data)) + "s"), data.encode())
        return self.file.write(data)

    def write_int(self, data: int) -> bool:
        """
        Write integer data to file
        """
        data = struct.pack(self.fmt_str("i"), data)
        return self.file.write(data)
