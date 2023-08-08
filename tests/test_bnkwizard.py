"""
Tests for BNKWizard class
"""

from modules.bnkwizard import BNKWizard


def test_bnkwizard_read():
    """
    Testing Reading a Bank File
    """
    bnkwizard = BNKWizard()
    bnkwizard_copy = BNKWizard()
    bnkwizard.read_bnk("data/dummy.bnk")
    bnkwizard_copy.read_bnk("data/dummy_copy.bnk")

    assert bnkwizard.bkhd_size == 32
    assert bnkwizard.didx_size == 12312
    assert bnkwizard.wem_array.wem_count == 1026
    assert bnkwizard.wem_array.wem_data_size == 22352891


def test_bnkwizard_write():
    """
    Testing Writing a Bank File
    """
    bnkwizard = BNKWizard()

    bnkwizard.read_bnk("data/dummy.bnk")
    bnkwizard.write_bnk("data/dummy_copy.bnk")
    with open("data/dummy.bnk", "rb") as orig_file, open(
        "data/dummy_copy.bnk", "rb"
    ) as dupl_file:
        assert orig_file.read() == dupl_file.read()


def test_bnkwizard_replace():
    """
    Testing Writing a Bank File
    """
    bnkwizard = BNKWizard()

    bnkwizard.read_bnk("data/dummy.bnk")
    bnkwizard.wem_array.add_replacement(
        bnkwizard.wem_array.wem_ids[0], "data/113946849.wem"
    )
    bnkwizard.write_bnk("data/dummy_new.bnk")
    bnkwizard_new = BNKWizard()
    bnkwizard_new.read_bnk("data/dummy_new.bnk")
    with open("data/113946849.wem", "rb") as wem_file:
        assert bnkwizard_new.wem_array.wems[0].data == wem_file.read()
        assert bnkwizard_new.wem_array.wems[1].data == bnkwizard.wem_array.wems[1].data
