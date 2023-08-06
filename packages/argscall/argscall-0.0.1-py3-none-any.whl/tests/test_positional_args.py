import pytest
from argscall import argsCaller
from argscall.exceptions import UnsupportedKeyArgument


# Function tha accepts positional arguments
def do_something(*args):
    return ":".join(args)


def test_missing_argument():
    a_caller = argsCaller(do_something)
    assert (a_caller.call()) == ""


def test_single_argument():
    assert argsCaller(do_something, "a").call() == "a"


def test_many_arguments():
    assert argsCaller(do_something, "a", "b", "c").call() == "a:b:c"


def test_keyword_arguments():
    with pytest.raises(UnsupportedKeyArgument) as pytest_wrapped_e:
        argsCaller(do_something, name="Joe")
    assert pytest_wrapped_e.value.argument_name == "name"
