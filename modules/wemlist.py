"""wem module"""
from dataclasses import dataclass
from modules.iostream import InputStream, OutputStream
from modules.audioutils import get_data_as_wem


@dataclass
class Wem:
    """WEM Class"""

    wem_id: int
    offset: int
    size: int
    data: bytes

    def __init__(self):
        pass


class WemList:
    """Class to store WEM Data"""

    def __init__(self):
        self.wem_count = None
        self.orig_wems = []
        self.repl_wems = []
        self.final_wems = []
        self.wem_ids = []
        self.rep_wem_ids = set()
        self.wem_id_idx_map = {}
        self.abs_offset = None

    def get_wem_metadata_from_bnk(self, inp: InputStream):
        """Read DIDX (Data Index) section into array"""
        didx_size = inp.read_int()
        if didx_size % 12 != 0:
            raise ValueError(
                "The file has a corrupted DIDX section! (its length is ",
                didx_size,
                ", which is not divisible by 12)",
            )
        self.wem_count = didx_size // 12
        self.orig_wems = [Wem() for _ in range(self.wem_count)]
        self.repl_wems = [Wem() for _ in range(self.wem_count)]
        self.final_wems = [Wem() for _ in range(self.wem_count)]
        for i in range(self.wem_count):
            (
                self.orig_wems[i].wem_id,
                self.orig_wems[i].offset,
                self.orig_wems[i].size,
            ) = [inp.read_int() for i in range(3)]
            self.wem_id_idx_map[self.orig_wems[i].wem_id] = i
            if i > 0 and self.orig_wems[i].offset < self.orig_wems[i - 1].offset:
                raise ValueError(
                    "The file has a corrupted DIDX section! (WEM number "
                    + i
                    + " is located at offset "
                    + self.orig_wems[i].offset
                    + ", while WEM number "
                    + (i - 1)
                    + " is located at offset "
                    + self.orig_wems[i - 1].offset
                    + ")"
                )
            self.wem_ids.append(self.orig_wems[i].wem_id)

    def get_wem_data_from_bnk(self, inp: InputStream):
        """Read DATA (Data) section into array"""
        data_size = inp.read_int()
        if data_size != self.orig_wems[-1].size + self.orig_wems[-1].offset:
            raise ValueError(
                "The file has a corrupted DATA section! (calculated length: ",
                sum(self.orig_wems[-1].size + self.orig_wems[-1].offset),
                ", actual length: ",
                data_size,
                ")",
            )
        self.abs_offset = inp.get_position()
        for i in range(self.wem_count):
            inp.set_position(self.abs_offset + self.orig_wems[i].offset)
            self.orig_wems[i].data = inp.read_bytes(self.orig_wems[i].size)

    def get_wem(self, wem_id: int, repl: bool = False) -> Wem:
        """Get WEM data given id"""
        idx = self.wem_id_idx_map[wem_id]
        if repl and wem_id in self.rep_wem_ids:
            return self.repl_wems[idx]
        return self.orig_wems[idx]

    def make_replacement(self, wem_id: int, new_wem: str):
        """Add replacement WEM"""
        wem_data = get_data_as_wem(new_wem)
        idx: int = self.wem_id_idx_map[wem_id]
        self.repl_wems[idx].data = wem_data
        self.repl_wems[idx].offset = self.orig_wems[idx].offset
        self.repl_wems[idx].size = len(wem_data)
        self.rep_wem_ids.add(wem_id)

    def remove_replacement(self, wem_id: int):
        """Remove replacement WEM"""
        self.rep_wem_ids.remove(wem_id)

    def create_final_wem_data(self):
        """Fill final data with replaced wems"""
        diff = 0
        for wem_id in self.wem_ids:
            idx: int = self.wem_id_idx_map[wem_id]
            if wem_id in self.rep_wem_ids:
                data = self.repl_wems[idx].data
                offset = self.repl_wems[idx].offset + diff
                size = self.repl_wems[idx].size
                diff = self.repl_wems[idx].size - self.orig_wems[idx].size
            else:
                data = self.orig_wems[idx].data
                offset = self.orig_wems[idx].offset + diff
                size = self.orig_wems[idx].size
            offset = ((offset // 16) + ((offset % 16) != 0)) * 16
            self.final_wems[idx].wem_id = wem_id
            self.final_wems[idx].data = data
            self.final_wems[idx].offset = offset
            self.final_wems[idx].size = size

    def clear_final_wem_data(self):
        """Clear final data after writing data"""
        self.final_wems = [Wem() for _ in range(self.wem_count)]

    def write_wem_metadata_to_bnk(self, out: OutputStream):
        """Write DIDX (Data Index) section into file"""
        out.write_int(self.wem_count * 12)
        for wem_id in self.wem_ids:
            idx: int = self.wem_id_idx_map[wem_id]
            out.write_int(self.final_wems[idx].wem_id)
            out.write_int(self.final_wems[idx].offset)
            out.write_int(self.final_wems[idx].size)

    def write_wem_data_to_bnk(self, out: OutputStream):
        """Write DATA (Data) section into file"""
        out.write_int(self.final_wems[-1].offset + self.final_wems[-1].size)
        for wem_id in self.wem_ids:
            idx: int = self.wem_id_idx_map[wem_id]
            out.set_position(self.abs_offset + self.final_wems[idx].offset)
            out.write_bytes(self.final_wems[idx].data)
