#!/usr/bin/env python
"""
Tests covering the parsing functions that read in light characteristics.
"""

import pytest


from light_character import light_character


@pytest.mark.parametrize(
    "test_input",
    [
        'F', 'Fl', 'LFl', 'Oc', 'Iso', 'Q'
    ]
)
def test_parse_pattern_simple(test_input):
    """
    Parse pattern returns the pattern name in lower case.
    If there are no explicit groups, there is an implicit single
    group of 1.
    """
    actual = light_character.parse_pattern(test_input)
    assert actual == (test_input.lower(), [1])


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ('F.', ('f', [1])),
        ('Fl.(3+1)', ('fl', [3, 1])),
        ('L.Fl.(2)', ('lfl', [2])),
        ('Oc.(1+2+3)', ('oc', [1, 2, 3]))
    ]
)
def test_parse_pattern(test_input, expected):
    """
    Parse pattern returns the pattern name in lower case, filtered for dots.
    If there are explicit groups, they are also returned.
    """
    assert light_character.parse_pattern(test_input) == expected


def test_period_error():
    try:
        light_character.parse_period([])
        assert False
    except IndexError:
        assert True


@pytest.mark.parametrize(
    "fragments,expected",
    [
        (['xyz', '1'], 1000),
        (['xyz', '10s'], 10000),
        (['xyz', '15', 's'], 15000),
        (['xyz', '1.5s'], 1500)
    ]
)
def test_period(fragments, expected):
    """
    The period is the last part of the characteristic.
    It may or may not be marked with 's' for seconds.
    The output value is in milliseconds.
    """
    assert light_character.parse_period(fragments) == expected


@pytest.mark.parametrize(
    "fragments,expected",
    [
        (['R'], 'R'),
        (['W'], 'W'),
        (['G', '1s'], 'G'),
        (['Y'], 'Y'),
    ]
)
def test_colour_code(fragments, expected):
    assert light_character.get_colour_code(fragments) == (
        expected,
        fragments[1:]
    )


def test_colour_code_default():
    """
    A characteristic without an explicit colour is white
    :return:
    """
    assert light_character.get_colour_code(['1s']) == (
        'W',
        ['1s']
    )
