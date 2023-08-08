"""
bnkwizard Module
"""
from modules.iostream import InputStream, OutputStream
from modules.wemarray import WEMArray


class BNKWizard:
    """
    BNKWizard Class
    """

    def __init__(self) -> None:
        self.bnk = None
        self.input_stream = None
        self.bkhd_size = None
        self.bkhd = None
        self.didx_size = None
        self.wem_array = WEMArray()
        self.abs_offset = None

    def read_bnk(self, bnk: str, little_endian: bool = True) -> None:
        """
        Load an existing BNK file and read its contents
        """
        self.bnk = bnk
        if self.input_stream:
            self.input_stream.close()
        self.input_stream = InputStream(bnk, little_endian)

        if self.input_stream.read_str(4) != "BKHD":
            raise ValueError("The file doesn't have a BKHD section!")
        self.bkhd_size = self.input_stream.read_int()
        self.bkhd = self.input_stream.read_bytes(self.bkhd_size)

        if self.input_stream.read_str(4) != "DIDX":
            raise ValueError("The file doesn't have a DIDX section!")
        self.didx_size = self.input_stream.read_int()
        if self.didx_size % 12 != 0:
            raise ValueError(
                "The file has a corrupted DIDX section! (its length is "
                + self.didx_size
                + ", which is not divisible by 12)"
            )

        self.wem_array.get_wem_metadata(self.input_stream, self.didx_size // 12)

        if self.input_stream.read_str(4) != "DATA":
            raise ValueError("The file doesn't have a DATA section!")
        data_size = self.input_stream.read_int()
        if data_size != self.wem_array.wem_data_size:
            raise ValueError(
                "The file has a corrupted DATA section! (calculated length: "
                + sum(self.wem_array.wem_data_size)
                + ", actual length: "
                + data_size
                + ")"
            )

        self.abs_offset = self.input_stream.get_position()

        self.wem_array.get_wem_data(self.input_stream, self.abs_offset)

    def write_bnk(self, bnk: str, little_endian: bool = True):
        """
        Create BNK file and write data to it
        """
        if self.bnk:
            output_stream = OutputStream(bnk, little_endian)

            output_stream.write_str("BKHD")
            output_stream.write_int(self.bkhd_size)
            output_stream.write_bytes(self.bkhd)

            output_stream.write_str("DIDX")
            self.wem_array.create_final_wem_data()
            self.wem_array.write_wem_metadata(output_stream)

            output_stream.write_str("DATA")
            self.wem_array.write_wem_data(output_stream, self.abs_offset)
            self.wem_array.clear_final_wem_data()
            rest = self.input_stream.read_bytes(-1)
            output_stream.write_bytes(rest)
            output_stream.close()
        else:
            raise ValueError("No source bank loaded!")

    def __del__(self):
        if self.input_stream:
            self.input_stream.close()
