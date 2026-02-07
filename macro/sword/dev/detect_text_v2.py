import pyautogui
import pytesseract
import cv2
import numpy as np
import time
import logging 

OCR_LANG = "kor+eng"
OCR_CONFIG = "--oem 1 --psm 6"

TYPE_INTERVAL = 0.5
FOCUS_DELAY = 1.2
ENTER_DELAY = 1.0
LOOP_INTERVAL = 5

logging.basicConfig(
    filename="ocr_detect.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def capture_and_ocr():
    screenshot = pyautogui.screenshot()
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    text = pytesseract.image_to_string(
        gray,
        lang=OCR_LANG,
        config=OCR_CONFIG
    )

    return text.splitlines()


def send_command(trigger: str):
    pyautogui.write(trigger, interval=TYPE_INTERVAL)
    pyautogui.press("space")
    pyautogui.press("backspace")

    time.sleep(ENTER_DELAY)

    pyautogui.press("enter")
    pyautogui.press("enter")


def detect_text_on_screen(loop_count: int, paused: bool) -> tuple[int, bool]:
    """
    loop_count: 현재 loop 번호
    paused: 대기 상태 여부
    return: (다음 loop_count, paused 상태)
    """
    lines = capture_and_ocr()
    time.sleep(FOCUS_DELAY)

    # stop / start 감지 (우선순위 최상)
    has_stop = any("stop" in line.lower() for line in lines)
    has_start = any("start" in line.lower() for line in lines)

    if has_stop and not paused:
        paused = True
        logging.info("[CONTROL] stop detected → paused")
        print("STOP 감지 → 대기 상태 진입")
        return loop_count, paused

    if has_start and paused:
        paused = False
        logging.info("[CONTROL] start detected → resumed")
        print("START 감지 → 대기 해제")
        return loop_count, paused

    # 대기 중이면 아무 동작도 안 함
    if paused:
        print(f"[loop={loop_count}] ⏸️ paused...")
        return loop_count, paused

    # 정상 강화/판매 로직
    matched_line = next(
        (
            line for line in lines
            if "[+10]" in line or "[+11]" in line
        ),
        None
    )

    if matched_line:
        print(f"[loop={loop_count}] yes (detected) → 판매")
        logging.info(f"[loop={loop_count}] SELL matched_line: {matched_line}")
        send_command(";s")
        return 1, paused
    else:
        print(f"[loop={loop_count}] no (not detected) → 강화")
        send_command(";g")
        return loop_count + 1, paused


if __name__ == "__main__":
    print("Auto 무기 강화 시작 (Ctrl + C 로 종료)")

    loop_count = 1
    paused = False

    try:
        while True:
            loop_count, paused = detect_text_on_screen(loop_count, paused)
            time.sleep(LOOP_INTERVAL)
    except KeyboardInterrupt:
        print("종료됨")
