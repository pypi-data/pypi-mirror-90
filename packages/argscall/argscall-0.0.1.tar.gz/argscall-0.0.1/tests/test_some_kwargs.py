import pytest
from argscall import argsCaller
from argscall.exceptions import UnsupportedKeyArgument, TooManyArgument, MissingArgument


# Function tha accepts a single position
def do_something(name):
    return name.upper()


def test_missing_argument():
    with pytest.raises(MissingArgument) as pytest_wrapped_e:
        argsCaller(do_something)
    assert pytest_wrapped_e.value.argument_name == "name"


def test_single_argument():
    assert argsCaller(do_something, "a").call() == "A"


def test_too_many_argument():
    with pytest.raises(TooManyArgument) as pytest_wrapped_e:
        argsCaller(do_something, "a", "b")
    assert pytest_wrapped_e.value.argument_value == "b"


def test_unsupported_keyword():
    with pytest.raises(UnsupportedKeyArgument) as pytest_wrapped_e:
        argsCaller(do_something, name='Joe', color="red")
    assert pytest_wrapped_e.value.argument_name == "color"
