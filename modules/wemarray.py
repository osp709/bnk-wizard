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
        self.rep_wems = []
        self.final_wems = []
        self.wem_ids = []
        self.rep_wem_ids = set()
        self.wem_id_idx_map = {}

    def get_wem_metadata_from_bnk(self, inp: InputStream, wem_count: int):
        """
        Read DIDX (Data Index) section into array
        """
        self.wem_count = wem_count
        self.wems = [self.WEM() for _ in range(self.wem_count)]
        self.rep_wems = [self.WEM() for _ in range(self.wem_count)]
        self.final_wems = [self.WEM() for _ in range(self.wem_count)]
        for i in range(self.wem_count):
            self.wems[i].wem_id, self.wems[i].offset, self.wems[i].size = [
                inp.read_int() for i in range(3)
            ]
            self.wem_id_idx_map[self.wems[i].wem_id] = i
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
            self.wem_ids.append(self.wems[i].wem_id)

    def add_replacement(self, wem_id: int, new_wem: str):
        """
        Add replacement WEM
        """
        with open(new_wem, "rb") as wem_f:
            wem_data = wem_f.read()
            idx: int = self.wem_id_idx_map[wem_id]
            self.rep_wems[idx].data = wem_data
            self.rep_wems[idx].offset = self.wems[idx].offset
            self.rep_wems[idx].size = len(wem_data)
            self.rep_wem_ids.add(wem_id)

    def remove_replacement(self, wem_id: int):
        """
        Add replacement WEM
        """
        self.rep_wem_ids.remove(wem_id)

    def get_wem_data_from_bnk(self, inp: InputStream, abs_offset: int):
        """
        Read DATA (Data) section into array
        """
        for i in range(self.wem_count):
            inp.set_position(abs_offset + self.wems[i].offset)
            self.wems[i].data = inp.read_bytes(self.wems[i].size)

    def create_final_wem_data(self):
        """
        Fill final data with replaced wems
        """
        diff = 0
        for wem_id in self.wem_ids:
            idx: int = self.wem_id_idx_map[wem_id]
            if wem_id in self.rep_wem_ids:
                data = self.rep_wems[idx].data
                offset = self.rep_wems[idx].offset + diff
                size = self.rep_wems[idx].size
                diff = self.rep_wems[idx].size - self.wems[idx].size
            else:
                data = self.wems[idx].data
                offset = self.wems[idx].offset + diff
                size = self.wems[idx].size
            offset = ((offset // 16) + ((offset % 16) != 0)) * 16
            self.final_wems[idx].wem_id = wem_id
            self.final_wems[idx].data = data
            self.final_wems[idx].offset = offset
            self.final_wems[idx].size = size

    def get_wem(self, wem_id: int) -> WEM:
        """
        Get WEM data given id
        """
        idx = self.wem_id_idx_map[wem_id]
        return self.wems[idx]

    def clear_final_wem_data(self):
        """
        Clear final data after writing data
        """
        self.final_wems = [self.WEM() for _ in range(self.wem_count)]

    def write_wem_metadata_to_bnk(self, out: OutputStream):
        """
        Write DIDX (Data Index) section into file
        """
        out.write_int(self.wem_count * 12)
        for wem_id in self.wem_ids:
            idx: int = self.wem_id_idx_map[wem_id]
            out.write_int(self.final_wems[idx].wem_id)
            out.write_int(self.final_wems[idx].offset)
            out.write_int(self.final_wems[idx].size)

    def write_wem_data_to_bnk(self, out: OutputStream, abs_offset: int):
        """
        Write DATA (Data) section into file
        """
        out.write_int(self.final_wems[-1].offset + self.final_wems[-1].size)
        for wem_id in self.wem_ids:
            idx: int = self.wem_id_idx_map[wem_id]
            out.set_position(abs_offset + self.final_wems[idx].offset)
            out.write_bytes(self.final_wems[idx].data)
