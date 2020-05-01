import pytest

from utils import value_update

def test_value_update():
    new_val, done = value_update(10, 100, 1)
    assert not done
    assert new_val >= 11

    new_val, done = value_update(9.9, 10, 1)
    assert done
    assert new_val == 10

    new_val, done = value_update(-9.9, -10, 1)
    assert done
    assert new_val == -10
