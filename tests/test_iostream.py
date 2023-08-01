"""
Tests for IOStream class
"""

from src.iostream import IOStream


def test_read_bytes():
    """
    Test for read_bytes
    """
    inp = IOStream("data/hello.txt")
    assert inp.read_bytes(-1) == "Hello World!".encode()


def test_read_string():
    """
    Test for read_string
    """
    inp = IOStream("data/hello.txt")
    assert inp.read_str(len("Hello World!")) == "Hello World!"


def test_read_int():
    """
    Test for read_int
    """
    inp = IOStream("data/hello.txt")
    assert inp.read_int() == 1819043144
