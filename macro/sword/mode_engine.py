import time
import re
import logging
from input import send_command
from parser import detect_hidden_weapon, should_enhance_hidden
from state import MacroState
from constants import MODE_LABEL

def _redact_hidden_name(msg: str) -> str:
    """
    로그 메시지에서 히든 무기 이름만 제거한다.
    """
    # 1) "히든 무기 감지됨: XXX"
    msg = re.sub(r"(히든 무기 감지됨:)\s*\S+", r"\1", msg)

    # 2) "→ XXX +10" / ": XXX +3 →"
    msg = re.sub(r"→\s*\S+\s*\+", "→ +", msg)
    msg = re.sub(r":\s*\S+\s*\+", ": +", msg)

    return msg

def log_info(msg: str, *, redact_hidden: bool = False):
    # 파일 로그는 항상 원문
    logging.info(msg)

    # # 콘솔 출력용 메시지
    # if redact_hidden:
    #     msg = _redact_hidden_name(msg)

    print(msg)

def mode_label(state):
    return MODE_LABEL.get(state.mode, state.mode)

def handle_enhance_cycle(
    state: MacroState,
    level: int,
    game_lines: list[str],
    *,
    needs_hidden: bool,
    auto_sell: bool,
    auto_pause: bool,
):
    detected_hidden = None

    # --- 히든 무기 탐지 ---
    if needs_hidden:
        detected_hidden = detect_hidden_weapon(game_lines)
        if detected_hidden:
            # 히든 상태는 항상 갱신
            state.prev_hidden_item = detected_hidden

            # 로그는 '초기 히든 감지 시점'에만
            should_log_hidden = (
                state.last_level is None or level == 1
            )

            if should_log_hidden:
                log_info(
                    f"[loop={state.loop}] [{mode_label(state)}] 히든 무기 감지됨: {detected_hidden}",
                    redact_hidden=True,
                )

    prev_hidden = state.prev_hidden_item
    hidden_name = prev_hidden or "무기"
    safe_level = state.last_level or 0
    target_reached = (
        (level == state.target)
        or (safe_level == state.target) 
        # or (safe_level - state.target < 2 and safe_level > state.target and level > 0)
    )

    # --- 목표 달성 ---
    if (not needs_hidden or prev_hidden) and target_reached:
        if auto_sell:
            log_info(
                f"[loop={state.loop}] [{mode_label(state)}] 목표 달성 → {hidden_name} +{level} 판매",
                redact_hidden=True,
            )
            send_command(";s")
            time.sleep(0.3)
            send_command(";g")
        elif auto_pause:
            log_info(
                f"[loop={state.loop}] [{mode_label(state)}] 목표 달성 → {hidden_name} +{level} 일시중지",
                redact_hidden=True,
            )
            state.paused = True

        state.prev_hidden_item = None
        state.last_level = None
        state.loop = 1
        return

    # --- 강화 시도 ---
    can_enhance = (
        not needs_hidden or
        (needs_hidden and prev_hidden and should_enhance_hidden(level, safe_level, state.target))
    )

    if can_enhance:
        if prev_hidden:
            log_info(
                f"[loop={state.loop}] [{mode_label(state)}] 히든 강화 시도: {hidden_name} +{level} → +{state.target}",
                redact_hidden=True,
            )
            send_command(";g")
        else:
            log_info(
                f"[loop={state.loop}] [{mode_label(state)}] 강화 시도: +{level} → +{state.target}"
            )
            send_command(";g")

        state.loop += 1

    # --- 히든 탐색 ---
    elif needs_hidden:
        log_info(
            f"[loop={state.loop}] [{mode_label(state)}] 히든무기 탐지중..."
        )
        send_command(";s")
        time.sleep(0.3)
        send_command(";g")
        state.prev_hidden_item = None
        state.last_level = None
        state.loop = 1

    if level > 0:
        state.last_level = level