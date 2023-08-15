"""sections: Module which contains the sections of bank"""

from modules.iostream import InputStream, OutputStream
from modules.wemlist import WemList


class BKHD:
    """BKHD Section Class"""

    header: str = "BKHD"
    size: int
    data: bytes

    def read_data(self, input_stream: InputStream):
        """Read data"""
        header = input_stream.read_str(4)
        if self.header != header:
            raise ValueError(self.header, " section not found!")
        self.size = input_stream.read_int()
        self.data = input_stream.read_bytes(self.size)

    def write_data(self, output_stream: OutputStream):
        """Write data"""
        output_stream.write_str(self.header)
        output_stream.write_int(self.size)
        output_stream.write_bytes(self.data)


class DIDX:
    """DIDX Section Class"""

    header: str = "DIDX"

    def read_data(self, input_stream: InputStream, wem_list: WemList):
        """Read data"""
        header = input_stream.read_str(4)
        if self.header != header:
            raise ValueError(self.header, " section not found!")
        wem_list.get_wem_metadata_from_bnk(input_stream)

    def write_data(self, output_stream: OutputStream, wem_list: WemList):
        """Write data"""
        output_stream.write_str(self.header)
        wem_list.write_wem_metadata_to_bnk(output_stream)


class DATA:
    """DATA Section Class"""

    header: str = "DATA"

    def read_data(self, input_stream: InputStream, wem_list: WemList):
        """Read data"""
        header = input_stream.read_str(4)
        if self.header != header:
            raise ValueError(self.header, " section not found!")
        wem_list.get_wem_data_from_bnk(input_stream)

    def write_data(self, output_stream: OutputStream, wem_list: WemList):
        """Write data"""
        output_stream.write_str(self.header)
        wem_list.write_wem_data_to_bnk(output_stream)


class HIRC:
    """HIRC Section Class"""

    header: str = "HIRC"
    size: int
    data: bytes

    def read_data(self, input_stream: InputStream):
        """Read data"""
        header = input_stream.read_str(4)
        if self.header != header:
            raise ValueError(self.header, " section not found!")
        self.size = input_stream.read_int()
        self.data = input_stream.read_bytes(self.size)

    def write_data(self, output_stream: OutputStream):
        """Write data"""
        output_stream.write_str(self.header)
        output_stream.write_int(self.size)
        output_stream.write_bytes(self.data)


class Sections:
    """To combine all sections into one wrapper"""

    bkhd = BKHD()
    didx = DIDX()
    data = DATA()
    hirc = HIRC()

    def read_sections(self, input_stream: InputStream, wem_list: WemList):
        """Read all sections"""
        self.bkhd.read_data(input_stream)
        self.didx.read_data(input_stream, wem_list)
        self.data.read_data(input_stream, wem_list)
        self.hirc.read_data(input_stream)

    def write_sections(self, output_stream: OutputStream, wem_list: WemList):
        """Write all sections"""
        self.bkhd.write_data(output_stream)
        self.didx.write_data(output_stream, wem_list)
        self.data.write_data(output_stream, wem_list)
        self.hirc.write_data(output_stream)
