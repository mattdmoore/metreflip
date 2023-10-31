import pytest

from metreflip.Rhythms import *


@pytest.fixture
def cycle_lengths():
    return [Rhythms(n) for n in range(12)]


def test_n(cycle_lengths):  # producing correct number of necklaces
    assert all([len(r) == n for r, n in zip(cycle_lengths, [1, 2, 3, 4, 6, 8, 14, 20, 36, 60, 108, 188, 352])])


def test_conversion(cycle_lengths):  # rhythms created from durations are the same as from positions
    for rhythms in cycle_lengths:
        assert all([Rhythm(rhythm.durations) == Rhythm(rhythm) for rhythm in rhythms])


def test_rotation(cycle_lengths):  # rotation doesn't break anything
    for rhythms in cycle_lengths:
        assert all([rhythm == Rhythm(rhythm.rotate(i).durations).rotate(-i)
                    for rhythm in rhythms for i, v in enumerate(rhythm) if v])


def test_indexing(cycle_lengths):  # converting to index matches necklace order
    for rhythms in cycle_lengths:
        assert all([int(rhythm) == i for i, rhythm in enumerate(rhythms)])
