from cycle import process_cycle_core
from constants import MODE_ENHANCE, MODE_SELL

def test_cycle_enhance_to_pause(base_state):
    game_lines = ["무기 강화 [+10]"]
    cmd_lines = []

    state = process_cycle_core(base_state, game_lines, cmd_lines)

    assert state.paused is True
    assert state.loop == 1

def test_cycle_mode_change_requires_pause(base_state):
    base_state.paused = False

    game_lines = []
    cmd_lines = ["sell"]

    state = process_cycle_core(base_state, game_lines, cmd_lines)

    # 모드 변경 안 됨
    assert state.mode == MODE_ENHANCE

def test_cycle_mode_change_when_paused(base_state):
    base_state.paused = True

    game_lines = []
    cmd_lines = ["sell"]

    state = process_cycle_core(base_state, game_lines, cmd_lines)

    assert state.mode == MODE_SELL