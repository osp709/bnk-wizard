"""
bnkwizard Module
"""
from iostream import IOStream


class BNKWizard:
    """
    BNKWizard Class
    """

    def __init__(self) -> None:
        self.input_stream = None
        self.bkhd_size = None
        self.bkhd = None
        self.didx_size = None
        self.wem_size = None

        self.ids = []
        self.offsets = []
        self.original_lengths = []
        self.replaced_lengths = []
        self.replacements = []

        self.data_size = None
        self.current_offset = None

    def read_bnk(self, bnk: str, little_endian: bool = True) -> None:
        """
        Load an existing BNK file and read its contents
        """
        if self.input_stream:
            self.input_stream.close()
        self.input_stream = IOStream(bnk, little_endian)

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

        self.wem_size = self.didx_size / 12
        for i in range(self.wem_size):
            wem_id, wem_offset, wem_length = [
                self.input_stream.read_int() for i in range(3)
            ]

            if i > 0 and wem_offset < self.offsets[i - 1]:
                raise ValueError(
                    "The file has a corrupted DIDX section! (WEM number "
                    + (i + 1)
                    + " is located at offset "
                    + wem_offset
                    + ", while WEM number "
                    + i
                    + " is located at offset "
                    + self.offsets[i - 1]
                    + ")"
                )

            self.ids.append(wem_id)
            self.offsets.append(wem_offset)
            self.original_lengths.append(wem_length)
            self.replaced_lengths.append(wem_length)

        if self.input_stream.read_str(4) != "DATA":
            raise ValueError("The file doesn't have a DATA section!")
        self.data_size = self.input_stream.read_int()
        if self.data_size < sum(self.original_lengths):
            raise ValueError(
                "The file has a corrupted DATA section! (calculated length: "
                + sum(self.original_lengths)
                + ", actual length: "
                + self.data_size
                + ")"
            )

        self.current_offset = self.input_stream.get_position()

    def write_bnk(self, bnk: str, little_endian: bool = True):
        """
        Create BNK file and write data to it
        """
        output_stream = IOStream(bnk, little_endian)

        output_stream.write_str("BKHD")
        output_stream.write_int(self.bkhd_size)
        output_stream.write_bytes(self.bkhd)

        output_stream.write_str("DIDX")
        output_stream.write_int(self.wem_size * 12)

        curr_address = 0
        for i in range(self.wem_size):
            output_stream.write_int(self.ids[i])
            output_stream.write_int(curr_address)
            output_stream.write_int(self.replaced_lengths[i])

            curr_address += self.replaced_lengths[i]

        output_stream.write_str("DATA")
        output_stream.write_int(sum(self.replaced_lengths))

        for i in range(self.wem_size):
            if self.replacements[i]:
                replacement = open(self.replacements[i], "rb")
                output_stream.write_bytes(replacement.read())

        rest = self.input_stream.read_bytes(-1)
        output_stream.write_bytes(rest)
        output_stream.close()

    def __del__(self):
        if self.input_stream:
            self.input_stream.close()
