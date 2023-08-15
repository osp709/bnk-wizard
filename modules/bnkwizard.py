"""
bnkwizard Module
"""
from modules.iostream import InputStream, OutputStream
from modules.wemlist import WemList
from modules.sections import Sections


class BNKWizard:
    """BNKWizard Class"""

    sections: Sections
    wem_list: WemList

    def read_bnk(self, bnk: str, little_endian: bool = True) -> None:
        """Load an existing BNK file and read its contents"""
        self.sections = Sections()
        self.wem_list = WemList()
        input_stream = InputStream(bnk, little_endian)
        self.sections.read_sections(input_stream, self.wem_list)
        input_stream.close()

    def write_bnk(self, bnk: str, little_endian: bool = True):
        """Create BNK file and write data to it"""
        output_stream = OutputStream(bnk, little_endian)
        self.wem_list.create_final_wem_data()
        self.sections.write_sections(output_stream, self.wem_list)
        output_stream.close()
