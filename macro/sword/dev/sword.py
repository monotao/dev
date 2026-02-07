import pyautogui
import pytesseract
import cv2
import numpy as np
import time
import logging
import re

RUN_MODE = "LIVE"

# ==================================================
# OCR 설정
# ==================================================
OCR_LANG_GAME = "kor+eng"
OCR_LANG_CMD  = "kor+eng"

OCR_CONFIG_GAME = (
    "--oem 1 --psm 6 "
    "-c load_system_dawg=0 "
    "-c load_freq_dawg=0"
)
OCR_CONFIG_CMD = (
    "--oem 1 --psm 6 "
    "-c load_system_dawg=0 "
    "-c load_freq_dawg=0"
    # "-c tessedit_char_whitelist=acdeghilnoprst0123456789+ "
)

# ==================================================
# 모드 정의
# ==================================================
MODE_ENHANCE = "enhance"
MODE_SELL    = "sell"
MODE_HIDDEN  = "hidden"
MODE_SEED  = "seed"

MODE_LABEL = {
    "enhance": "강화모드",
    "sell": "판매모드",
    "hidden": "히든모드",
    "seed": "시드모드",
}

# ==================================================
# 히든 무기 키워드
# ==================================================
HIDDEN_KEYWORDS = [
    "광선검", "지킨 검", "심판검", "불의 검", "빛의 검",
    "슬리퍼", "샌들", "신발",
    "꽃다발", "다발", "에덴동산", "오르페우스",
    "우산", "천막", "방패", "아이기스 원형", "아이기스",
    "젓가락", "비도", "반고가 세상",
    "소시지", "핫도그",
    "칫솔", "치솔", "칫소", "치소", "털이", "곰팡이", "치약", "포자", "치아", "이빨",
    "빗자루", "주전자", "단소", "브레드",
    "채찍", "붉은 끈", "붉은 꼬리", "고삐", "붉은 기수", "핏빛 날개", "가르는 꼬리", "붉은 혜성", "삼킨 적토마", "말의 궤적", "붉은 짐승",
    "기타", "유발자", "앰프", "디스토션", "피드백", "영혼을 켜는 악기", "광란의 지배자", "레퀴엠", "심연 현", "진짜 리라", "계약서", "뇌명 제우스", "초끈", "빅뱅의 시발점", "공명 주파수", "벤딩", "지휘자", "적막 소리의 종언",
    "하드", "3초 룰", "프리즈", "액체질소", "와사비", "녹차", "초콜릿", "바닐라", "쿠키", "융단폭격", "민트초코", "파이퍼", "엑스칼리", "설탕", "밀크", "아이스바", "파르페"
]

# ==================================================
# 타이밍 설정
# ==================================================
TYPE_INTERVAL = 0.3
FOCUS_DELAY   = 0.1
ENTER_DELAY   = 0.3
LOOP_INTERVAL = 3.1

MODE_RUNTIME_CONFIG = {
    MODE_SEED: {"loop_interval": 3.1},
    MODE_HIDDEN: {"loop_interval": 3.1},
    MODE_SELL: {"loop_interval": 3.1},
    MODE_ENHANCE: {"loop_interval": 3.1},
}


# ==================================================
# 로그 설정
# ==================================================
logging.basicConfig(
    filename="ocr_detect.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# ==================================================
# OCR
# ==================================================
def capture_and_ocr(lang: str, config: str) -> list[str]:
    screenshot = pyautogui.screenshot()
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    text = pytesseract.image_to_string(gray, lang=lang, config=config)
    return [line.strip() for line in text.splitlines() if line.strip()]

# ==================================================
# 키 입력
# ==================================================
def send_command(cmd: str):
    pyautogui.write(cmd, interval=TYPE_INTERVAL)
    pyautogui.press("space")
    pyautogui.press("backspace")
    time.sleep(ENTER_DELAY)
    pyautogui.press("enter")
    pyautogui.press("enter")

# ==================================================
# 파싱 유틸
# ==================================================
def extract_enhance_level(lines: list[str]) -> int | None:
    for line in lines:
        m = re.search(r"\[\+(\d+)", line)
        if m:
            value = int(m.group(1))
            if value > 20:
                logging.info(f"[안내] 강화 수치 OCR 이상치 무시: value={value}")
                return None
            return value
    return None


def detect_hidden_weapon(lines: list[str]) -> str | None:
    for line in lines:
        for kw in HIDDEN_KEYWORDS:
            if kw in line:
                return kw
    return None


def detect_mode(cmd_lines: list[str], current_mode: str):
    for line in cmd_lines:
        m = re.search(r"(enhance|hidden|seed|sell)", line)
        if m:
            return m.group(1), line
    return current_mode, None


def parse_levels(cmd_lines, target):
    for line in cmd_lines:
        m = re.search(r"target\s*\+?\s*(\d+)", line)
        if m:
            new_target = int(m.group(1))
            if new_target != target:
                logging.info(
                    # f"[안내] 목표변경 {target} → {new_target} | line='{line}'"
                    f"[안내] 목표변경 {target} → {new_target}"
                )
            target = new_target
    return target


def detect_control(cmd_lines, paused):
    has_stop = any("stop" in line for line in cmd_lines)
    has_start = any("start" in line for line in cmd_lines)

    if has_stop:
        if not paused:
            logging.info("[안내] stop → paused")
            print("[안내] 매크로 일시중지")
        return True

    if has_start:
        if paused:
            logging.info("[안내] start → resumed")
            print("[안내] 매크로 재개")
        return False
    return paused


def should_enhance_hidden(level, safe_level, target):
    if level == 0:
        return True
    if (safe_level <= target) and (level >= safe_level):
        return True
    return False

# ==================================================
# 메인 사이클
# ==================================================
def process_cycle_core(
    state: dict,
    game_lines: list[str],
    cmd_lines: list[str],
) -> dict:

    # print("[DEBUG] game_lines =", game_lines)
    # print("[DEBUG] cmd_lines  =", cmd_lines)

    # ---- control (항상 처리) ----
    state["paused"] = detect_control(cmd_lines, state["paused"])

    new_mode, mode_line = detect_mode(cmd_lines, state["mode"])

    if new_mode != state["mode"]:
        if state["paused"]:
            prev_mode = state["mode"]
            state["mode"] = new_mode

            logging.info(f"[안내] {prev_mode} → {state['mode']} | line='{mode_line}'")
            # print(f"[안내] {prev_mode} → {state['mode']} (paused)")
            # if mode_line:
            #     print(f"  ↳ from line: {mode_line}")

        else:
            logging.info(f"[안내] 모드 변경불가 - 일시정지시 가능 | 요청한 모드={new_mode} | 현재모드={state['mode']}")
            print(f"[안내] 모드 변경불가 - 일시정지시 가능 | 요청한 모드={new_mode} | 현재모드={state['mode']}")

    state["target"] = parse_levels(cmd_lines, state["target"])

    # 실행만 막기
    if state["paused"]:
        mode_label = MODE_LABEL.get(state["mode"])
        state["loop"] = 1
        print(f"[loop={state['loop']}] paused | mode={mode_label} | target={state['target']}")
        return state

    tmp_level = extract_enhance_level(game_lines)
    level = tmp_level if tmp_level is not None else 0

    # ---- MODE_ENHANCE ----
    if state["mode"] == MODE_ENHANCE:
        last_level = state.get("last_hidden_level")
        safe_level = last_level if last_level is not None else 0        
        if state["target"] in (level, safe_level):
            state["paused"] = True
            logging.info(f"[loop={state['loop']}] [강화모드] 목표 달성! 무기 +{level} → 일시중지")
            print(f"[loop={state['loop']}] [강화모드] 목표 달성! 무기 +{level} → 일시중지")
            state["safe_level"] = 0
            state["loop"] = 1
        else:
            send_command(";g")
            logging.info(f"[loop={state['loop']}] [강화모드] 강화 시도! 무기 +{level} → +{state['target']}")
            print(f"[loop={state['loop']}] [강화모드] 강화 시도! 무기 +{level} → +{state['target']}")
            state["loop"] += 1
        if level > 0:
            state["last_hidden_level"] = level

    # ---- MODE_SELL ----
    elif state["mode"] == MODE_SELL:
        last_level = state.get("last_hidden_level")
        safe_level = last_level if last_level is not None else 0              
        if state["target"] in (level, safe_level):
            send_command(";s")
            send_command(";g")
            logging.info(f"[loop={state['loop']}] [판매모드] 목표 달성! 무기 +{level} → 판매")
            print(f"[loop={state['loop']}] [판매모드] 목표 달성! 무기 +{level} → 판매")
            state["safe_level"] = 0
            state["loop"] = 1
        else:
            send_command(";g")
            logging.info(f"[loop={state['loop']}] [판매모드] 강화 시도! 무기 +{level} → +{state['target']}")
            print(f"[loop={state['loop']}] [판매모드] 강화 시도! 무기 +{level} → +{state['target']}")
            state["loop"] += 1
        if level > 0:
            state["last_hidden_level"] = level

    # ---- MODE_HIDDEN ----
    elif state["mode"] == MODE_HIDDEN:
        hidden_item = detect_hidden_weapon(game_lines)
        prev_hidden_item = state.get("prev_hidden_item")

        # 히든 무기 감지되었으면 상태 기억
        if hidden_item:
            state["prev_hidden_item"] = hidden_item
            prev_hidden_item = hidden_item

        last_level = state.get("last_hidden_level")
        safe_level = last_level if last_level is not None else 0

        # 1 히든 무기 + 목표 달성 → 일시중지
        if prev_hidden_item and state["target"] in (level, safe_level):
            state["paused"] = True
            logging.info(f"[loop={state['loop']}] [히든모드] 목표 달성! '{hidden_item}' +{level} → 일시중지")
            print(f"[loop={state['loop']}] [히든모드] 목표 달성! 히든무기 +{level} → 일시중지")
            state["prev_hidden_item"] = None
            state["safe_level"] = 0
            state["loop"] = 1
        # 2) 히든 무기 + 아직 목표 미달 → 강화
        elif prev_hidden_item and should_enhance_hidden(level, safe_level, state['target']):
            send_command(";g")
            logging.info(f"[loop={state['loop']}] [히든모드] 강화 시도! '{hidden_item}' +{safe_level+1} → +{state['target']}, {prev_hidden_item} +{level} +{safe_level}" )
            print(f"[loop={state['loop']}] [히든모드] 강화 시도! 히든무기 +{safe_level+1} → +{state['target']}")
            state["loop"] += 1
        # 3) 히든 무기 없음 → 탐색
        else:
            logging.warning(f"[히든모드] '{prev_hidden_item}' +{safe_level} → 탐색 전환, {level} {safe_level}" )
            send_command(";s")
            send_command(";g")
            logging.info(f"[loop={state['loop']}] [히든모드] 히든무기 탐지중...")
            print(f"[loop={state['loop']}] [히든모드] 히든무기 탐지중...")
            state["prev_hidden_item"] = None            
            state["loop"] = 1
        # 마지막 level 저장
        if level > 0:
            state["last_hidden_level"] = level

    # ---- MODE_SEED ----
    elif state["mode"] == MODE_SEED:
        hidden_item = detect_hidden_weapon(game_lines)
        prev_hidden_item = state.get("prev_hidden_item")

        if hidden_item:
            state["prev_hidden_item"] = hidden_item
            prev_hidden_item = hidden_item

        last_level = state.get("last_hidden_level")
        safe_level = last_level if last_level is not None else 0

        if prev_hidden_item and state["target"] in (level, safe_level):
            send_command(";s")
            send_command(";g")
            logging.info(f"[loop={state['loop']}] [시드모드] 목표 달성! '{hidden_item}' +{level} → 판매")
            print(f"[loop={state['loop']}] [시드모드] 목표 달성! 히든무기 +{level} → 판매")
            state["prev_hidden_item"] = None
            state["safe_level"] = 0
            state["loop"] = 1
        elif prev_hidden_item and should_enhance_hidden(level, safe_level, state['target']):
            send_command(";g")
            logging.info(f"[loop={state['loop']}] [시드모드] 강화 시도! 강화 시도! '{hidden_item}' +{safe_level+1} → +{state['target']}, {prev_hidden_item} {level} {safe_level}" )
            print(f"[loop={state['loop']}] [시드모드] 강화 시도! 히든무기 +{level} → +{state['target']}")
            state["loop"] += 1
        else:
            logging.warning(f"[시드모드] '{prev_hidden_item}' +{safe_level} → 탐색 전환, {level} {safe_level}")
            send_command(";s")
            send_command(";g")
            logging.info(f"[loop={state['loop']}] [시드모드] 히든무기 탐지중...")
            print(f"[loop={state['loop']}] [시드모드] 히든무기 탐지중...")
            state["prev_hidden_item"] = None            
            state["loop"] += 1
        if level > 0:
            state["last_hidden_level"] = level
    return state


def process_cycle(state: dict) -> dict:
    game_lines = capture_and_ocr(OCR_LANG_GAME, OCR_CONFIG_GAME)
    cmd_lines  = capture_and_ocr(OCR_LANG_CMD,  OCR_CONFIG_CMD)
    time.sleep(FOCUS_DELAY)

    return process_cycle_core(state, game_lines, cmd_lines)


def test_process_cycle(
    state: dict,
    game_lines: list[str],
    cmd_lines: list[str],
) -> dict:
    print("game_lines =", game_lines)
    print("cmd_lines  =", cmd_lines)

    return process_cycle_core(state, game_lines, cmd_lines)


def print_test_process_cycle():
    print("\n=== print_test_process_cycle ===")

    scenarios = [
        # (game_lines, cmd_lines)
        ([], []),
        (["무기 강화 [+9]"], []),
        (["무기 강화 [+9]"], ["target 10"]),
        (["무기 강화 [+10]"], []),
        (["실패"], ["start"]),
        (["실패"], ["stop"]),
        (["실패"], ["start"]),
        ([], ["sell"]),
        (["무기 강화 [+10]"], ["sell"]),
        ([], ["hidden"]),
        (["광선검"], ["hidden"]),
        (["실패"], ["start"]),
        (["광선검"], ["enhance"]),
    ]

    state = {
        "paused": False,
        "mode": MODE_ENHANCE,
        "target": 10,
        "loop": 1,
    }

    for i, (game_lines, cmd_lines) in enumerate(scenarios, 1):
        print(f"\n--- cycle {i} ---")
        # print("game_lines =", game_lines)
        # print("cmd_lines  =", cmd_lines)

        state = test_process_cycle(state, game_lines, cmd_lines)
        print("state =", state)

# ==================================================
# main
# ==================================================
if __name__ == "__main__":

    if RUN_MODE == "LIVE":
        print("[안내] 자동 무기 강화 매크로 시작 (Ctrl + C 종료)")

        state = {
            "paused": False,
            "mode": MODE_ENHANCE,
            "target": 10,
            "loop": 1,
        }

        try:
            while True:
                # ode별 런타임 설정 적용
                cfg = MODE_RUNTIME_CONFIG.get(state["mode"])
                if cfg:
                    loop_interval = cfg["loop_interval"]
                else:
                    loop_interval = LOOP_INTERVAL  # fallback

                state = process_cycle(state)
                time.sleep(loop_interval)

        except KeyboardInterrupt:
            print("[안내] 종료됨")

    elif RUN_MODE == "TEST":
        print("=== TEST MODE ===")
        print_test_process_cycle()