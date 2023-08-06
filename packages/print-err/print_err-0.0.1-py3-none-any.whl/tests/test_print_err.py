import pytest
from print_err import print_err


def test_print_err(capsys):
    print_err("Test printing to stderr")
    outerr = capsys.readouterr()
    assert outerr.out == ""
    assert outerr.err == "Test printing to stderr\n"


def test_extra_args(capsys):
    print_err("Test printing to stderr", end="")
    outerr = capsys.readouterr()
    assert outerr.out == ""
    assert outerr.err == "Test printing to stderr"


def test_exit_code(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        print_err("Test printing to stderr", exit_code=2)
    outerr = capsys.readouterr()
    assert outerr.out == ""
    assert outerr.err == "Test printing to stderr\n"
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2
