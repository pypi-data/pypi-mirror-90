from __future__ import division
import pytest

from stringtopy import str_to_float_converter


def test_not_float(default_str_to_float):
    with pytest.raises(ValueError):
        default_str_to_float("this is not a float")

def test_not_float_with_none():
    str_to_float = str_to_float_converter(use_none_on_fail=True)
    assert str_to_float("this is not a float") is None

def test_decimal(default_str_to_float):
    assert default_str_to_float("1.234") == 1.234

def test_exp_notation(default_str_to_float):
    assert default_str_to_float("5.76e7") == 5.76e7

def test_fraction(default_str_to_float):
    assert 3 / 2 == default_str_to_float("3/2")

@pytest.mark.xfail
def test_fraction_with_spaces(default_str_to_float):
    assert 3 / 2 == default_str_to_float("3 / 2")
