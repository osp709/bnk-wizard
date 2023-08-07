"""
wem module
"""
import dataclasses
from modules.iostream import InputStream, OutputStream


class WEMArray:
    """
    Class to store WEM Data
    """

    @dataclasses.dataclass
    class WEM:
        """
        WEM Class
        """

        wem_id: int
        offset: int
        size: int
        data: bytes

        def __init__(self):
            pass

    def __init__(self):
        self.wem_count = None
        self.wems = []
        self.wem_data_size = 0

    def get_wem_metadata(self, inp: InputStream, wem_count: int):
        """
        Read DIDX (Data Index) section into array
        """
        self.wem_count = wem_count
        self.wems = [self.WEM() for _ in range(self.wem_count)]
        for i in range(self.wem_count):
            self.wems[i].wem_id, self.wems[i].offset, self.wems[i].size = [
                inp.read_int() for i in range(3)
            ]
            if i > 0 and self.wems[i].offset < self.wems[i - 1].offset:
                raise ValueError(
                    "The file has a corrupted DIDX section! (WEM number "
                    + i
                    + " is located at offset "
                    + self.wems[i].offset
                    + ", while WEM number "
                    + (i - 1)
                    + " is located at offset "
                    + self.wems[i - 1].offset
                    + ")"
                )
        self.wem_data_size = self.wems[-1].offset + self.wems[-1].size

    def get_wem_data(self, inp: InputStream, abs_offset: int):
        """
        Read DATA (Data) section into array
        """
        for i in range(self.wem_count):
            inp.set_position(abs_offset + self.wems[i].offset)
            self.wems[i].data = inp.read_bytes(self.wems[i].size)

    # TODO : Replace wem_data
    def replace_wem_data(self, new_wem: str):
        """
        Replace a particular WEM data with new WEM data
        """

    def write_wem_metadata(self, out: OutputStream):
        """
        Write DIDX (Data Index) section into file
        """
        out.write_int(self.wem_count * 12)
        for wem in self.wems:
            out.write_int(wem.wem_id)
            out.write_int(wem.offset)
            out.write_int(wem.size)

    def write_wem_data(self, out: OutputStream, abs_offset: int):
        """
        Write DATA (Data) section into file
        """
        out.write_int(self.wems[-1].offset + self.wems[-1].size)
        for wem in self.wems:
            out.set_position(abs_offset + wem.offset)
            out.write_bytes(wem.data)
