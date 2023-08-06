import pytest
from argscall import argsCaller
from argscall.exceptions import TooManyArgument


# Function that requires
def do_something():
    return "A"


# Function with a default value
def do_something_default(name="Joe"):
    return name.upper()


def test_no_arguments():
    assert argsCaller(do_something).call() == "A"


def test_default_argument():
    assert argsCaller(do_something_default).call() == "JOE"


def test_too_many_arguments():
    with pytest.raises(TooManyArgument) as pytest_wrapped_e:
        argsCaller(do_something, "a")
    assert pytest_wrapped_e.value.argument_value == "a"
