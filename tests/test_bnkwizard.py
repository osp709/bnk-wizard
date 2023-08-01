"""
Tests for BNKWizard class
"""

from src.bnkwizard import BNKWizard


def test_bnkwizard():
    bnkwizard = BNKWizard()

    bnkwizard.read_bnk("data/dummy.bnk")

    assert bnkwizard.didx_size % 12 == 0
