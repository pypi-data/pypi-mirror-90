import pytest
from argscall import argsCaller
from argscall.exceptions import TooManyArgument


# Function tha accepts positional arguments
def do_something(**kwargs):
    return ":".join([str(k) + str(v) for k, v in kwargs.items()])


def test_missing_argument():
    a_caller = argsCaller(do_something)
    assert (a_caller.call()) == ""


def test_single_argument():
    with pytest.raises(TooManyArgument) as pytest_wrapped_e:
        assert argsCaller(do_something, "a")
    assert pytest_wrapped_e.value.argument_value == "a"


def test_single_kwargument():
    assert argsCaller(do_something, a=12).call() == "a12"


def test_many_kwarguments():
    assert argsCaller(do_something, a=12, b=15, c=5).call() == "a12:b15:c5"
