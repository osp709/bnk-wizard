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

    assert (
        open("data/dummy.bnk", "rb").read() == open("data/dummy_copy.bnk", "rb").read()
    )
