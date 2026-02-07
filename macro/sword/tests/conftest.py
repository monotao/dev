import pytest
from state import MacroState
from constants import MODE_ENHANCE

@pytest.fixture
def base_state():
    return MacroState(
        paused=False,
        mode=MODE_ENHANCE,
        target=10,
        loop=1,
    )