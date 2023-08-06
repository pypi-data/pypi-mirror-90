#!/usr/bin/env python

import pytest


from light_character import light_character


def test_fixed():
    """
    Fixed characters are just on. Groups and Period are ignored.
    For compatibility downstream, they are given a period of 1
    """
    assert light_character.fixed(None, 'R', None) == [('R', 1)]


@pytest.mark.parametrize(
    "period,on,off",
    [
        (1000, 500, 500),
        (1600, 800, 800),
        (8000, 4000, 4000),
        # An odd number is an unlikely scenario, as the top-level input is
        # in seconds, but by now it has been converted to milliseconds.
        # Theoretically, you could provide a period of 1.1111s
        (15, 7, 8)
    ]
)
def test_isophase(period, on, off):
    assert light_character.isophase(None, 'G', period) == [
        ('G', on),
        ('Off', off)
    ]


def test_single_flash():
    """
    A single flash is 1 second long
    """
    assert light_character.flash(
        [1], 'R', 5000
    ) == [('R', 1000), ('Off', 4000)]


def test_group_flash():
    """
    In a group, the flashes are shorter (0.5 seconds) long. The period between
    individual flashes in a group are 1 second
    """
    assert light_character.flash([2], 'R', 5000) == [
        ('R', 500), ('Off', 1000),
        ('R', 500), ('Off', 1000),
        ('Off', 2000)
    ]


def test_composite_group_flash():
    """
    In a composite group, the flashes are shorter (0.5 seconds) long.
    The period between individual flashes in a group are 1 second.
    The spare time is distributed evenly after each group
    """
    assert light_character.flash([3, 1], 'R', 10000) == [
        ('R', 500), ('Off', 1000),
        ('R', 500), ('Off', 1000),
        ('R', 500), ('Off', 1000),
        ('Off', 2000),
        ('R', 500), ('Off', 1000),
        ('Off', 2000)
    ]


def test_single_occult():
    """
    A single occult is 1 second long
    """
    assert light_character.occulting(
        [1], 'G', 5000
    ) == [('Off', 1000), ('G', 4000)]


def test_group_occult():
    """
    In a group, the occults are shorter (0.5 seconds) long. The period between
    individual occults in a group are 1 second
    """
    assert light_character.occulting([2], 'G', 5000) == [
        ('Off', 500), ('G', 1000),
        ('Off', 500), ('G', 1000),
        ('G', 2000)
    ]


def test_composite_group_occult():
    """
    In a composite group, the occults are shorter (0.5 seconds) long.
    The period between individual occults in a group are 1 second.
    The spare time is distributed evenly after each group
    """
    assert light_character.occulting([3, 1], 'G', 10000) == [
        ('Off', 500), ('G', 1000),
        ('Off', 500), ('G', 1000),
        ('Off', 500), ('G', 1000),
        ('G', 2000),
        ('Off', 500), ('G', 1000),
        ('G', 2000)
    ]


def test_single_long_flash():
    """
    A single long flash is 2 second long
    """
    assert light_character.long_flash(
        [1], 'Y', 6000
    ) == [('Y', 2000), ('Off', 4000)]


def test_group_long_flash():
    """
    The defining feature of a long flash is that it is alight for 2 seconds
    or more. So the flashes are not shortened in a group context
    """
    assert light_character.long_flash([2], 'R', 15000) == [
        ('R', 2000), ('Off', 3000),
        ('R', 2000), ('Off', 3000),
        ('Off', 5000)
    ]


def test_composite_group_long_flash():
    """
    The period between individual flashes in a group are 3 seconds.
    The spare time is distributed evenly after each group
    """
    assert light_character.long_flash([2, 1], 'R', 20000) == [
        ('R', 2000), ('Off', 3000),
        ('R', 2000), ('Off', 3000),
        ('Off', 2500),
        ('R', 2000), ('Off', 3000),
        ('Off', 2500)
    ]
    
    
def test_single_quick_flash():
    """
    A single quick flash is 0.25 seconds long
    """
    assert light_character.quick(
        [1], 'Y', None
    ) == [('Y', 250), ('Off', 750)]

