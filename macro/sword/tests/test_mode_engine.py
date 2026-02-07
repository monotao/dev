import mode_engine
from constants import MODE_CONFIG, MODE_HIDDEN, MODE_ENHANCE

def test_enhance_pause_on_target_reached(monkeypatch, base_state):
    calls = []

    monkeypatch.setattr(
        mode_engine,
        "send_command",
        lambda cmd: calls.append(cmd)
    )

    base_state.mode = MODE_ENHANCE
    level = 10

    cfg = MODE_CONFIG[MODE_ENHANCE]

    mode_engine.handle_enhance_cycle(
        base_state,
        level,
        game_lines=["무기 강화 [+10]"],
        **cfg,
    )

    assert base_state.paused is True
    assert calls == []  # 강화/판매 없음

def test_hidden_sell_on_target(monkeypatch, base_state):
    calls = []

    monkeypatch.setattr(
        mode_engine,
        "send_command",
        lambda cmd: calls.append(cmd)
    )

    base_state.mode = MODE_HIDDEN
    base_state.target = 5
    base_state.prev_hidden_item = "광선검"
    base_state.last_hidden_level = 5

    cfg = MODE_CONFIG[MODE_HIDDEN]

    mode_engine.handle_enhance_cycle(
        base_state,
        level=5,
        game_lines=["광선검"],
        **cfg,
    )

    # hidden + auto_pause
    assert base_state.paused is True
    assert calls == []