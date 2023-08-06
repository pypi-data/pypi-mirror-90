from argscall import argsCaller
from argscall.exceptions import MissingArgument, TooManyArgument
import pytest


def do_something(name):
    return name.upper()


def do_something_default(name, family="Black"):
    return f"{name} {family}"


def test_single_argument():
    assert argsCaller(do_something, "a").call() == "A"


def test_single_default_argument():
    assert argsCaller(do_something_default, "Joe").call() == "Joe Black"


def test_missing_argument():
    with pytest.raises(MissingArgument) as pytest_wrapped_e:
        argsCaller(do_something)
    assert pytest_wrapped_e.value.argument_name == "name"


# Call the function with an extra arguments
def test_too_many_arguments():
    with pytest.raises(TooManyArgument) as pytest_wrapped_e:
        argsCaller(do_something, "a", "b")
    assert pytest_wrapped_e.value.argument_value == "b"
