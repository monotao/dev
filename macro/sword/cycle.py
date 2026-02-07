import time
from ocr import capture_and_ocr_roi
from parser import (
    extract_enhance_level,
    detect_mode,
    parse_levels,
    detect_control,
)
from mode_engine import handle_enhance_cycle, log_info
from state import MacroState
from constants import (
    MODE_CONFIG, MODE_LABEL, FOCUS_DELAY,
    OCR_LANG_GAME, OCR_CONFIG_GAME, GAME_ROI,
    OCR_LANG_CMD, OCR_CONFIG_CMD, CMD_ROI,
)

def mode_label(mode: str):
    return MODE_LABEL.get(mode, mode)

def process_cycle_core(
    state: MacroState,
    game_lines: list[str],
    cmd_lines: list[str],
) -> MacroState:

    state.paused = detect_control(cmd_lines, state.paused)

    new_mode, _ = detect_mode(cmd_lines, state.mode)
    if new_mode != state.mode:
        if state.paused:
            current_mode = state.mode
            log_info(f"[안내] {mode_label(current_mode)} → {mode_label(new_mode)} | 현재모드={mode_label(current_mode)} | 요청한 모드={mode_label(new_mode)}" )
            state.mode = new_mode
        else:
            log_info(f"[안내] 모드 변경은 pause 상태에서만 가능 | 요청한 모드={mode_label(new_mode)}")

    state.target = parse_levels(cmd_lines, state.target)

    if state.paused:
        label = MODE_LABEL.get(state.mode)
        log_info(f"[paused] mode={label} | target={state.target}")
        state.loop = 1
        return state

    tmp = extract_enhance_level(game_lines)
    level = tmp if tmp is not None else 0

    cfg = MODE_CONFIG[state.mode]
    handle_enhance_cycle(
        state,
        level,
        game_lines,
        **cfg,
    )
    return state

def process_cycle(state: MacroState) -> MacroState:
    # game_lines = capture_and_ocr_roi(GAME_ROI, lang=OCR_LANG_GAME, config=OCR_CONFIG_GAME)
    # cmd_lines  = capture_and_ocr_roi(CMD_ROI, lang=OCR_LANG_CMD,  config=OCR_CONFIG_CMD)
    lines = capture_and_ocr_roi(GAME_ROI, lang=OCR_LANG_GAME, config=OCR_CONFIG_GAME)
    time.sleep(FOCUS_DELAY)
    return process_cycle_core(state, lines, lines)