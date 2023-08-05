"""
Tests for IOStream class
"""

from modules.iostream import InputStream, OutputStream


def test_read_bytes():
    """
    Test for read_bytes
    """
    res = "Hello World!".encode()
    with open("data/hello", "wb") as f:
        f.write(res)
    inp = InputStream("data/hello")
    assert inp.read_bytes(-1) == res
    inp.close()


def test_read_string():
    """
    Test for read_string
    """
    res = "Hello World!"
    with open("data/hello", "w") as f:
        f.write(res)
    inp = InputStream("data/hello")
    assert inp.read_str(len("Hello World!")) == res
    inp.close()


def test_read_int():
    """
    Test for read_int
    """
    res = 12
    with open("data/hello", "wb") as f:
        f.write(res.to_bytes(length=4, byteorder="little"))
    inp = InputStream("data/hello")
    assert inp.read_int() == res
    inp.close()


def test_write_bytes():
    """
    Test for write_bytes
    """
    out = OutputStream("data/bye")
    res = "Bye World!".encode()
    out.write_bytes(res)
    out.close()
    with open("data/bye", "rb") as f:
        assert f.read() == res


def test_write_string():
    """
    Test for write_string
    """
    out = OutputStream("data/bye")
    res = "Bye World!"
    out.write_str(res)
    out.close()
    with open("data/bye", "rb") as f:
        assert f.read().decode() == res


def test_write_int():
    """
    Test for write_int
    """
    out = OutputStream("data/bye")
    res = 123
    out.write_int(res)
    out.close()
    with open("data/bye", "rb") as f:
        assert int.from_bytes(f.read(), "little") == res
