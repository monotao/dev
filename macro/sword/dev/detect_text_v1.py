import pyautogui
import pytesseract
import cv2
import numpy as np
import time

def detect_text_on_screen():
    screenshot = pyautogui.screenshot()
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(
        gray, 0, 255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    custom_config = r"""
        --oem 3
        --psm 6
    """

    extracted_text = pytesseract.image_to_string(
        gray,
        lang="kor+eng",
        config=custom_config
    )

    lines = extracted_text.splitlines()

    matched_lines = [
        line for line in lines
        if "+11]" in line
        # if "+11]" in line and "속보" in line
    ]

    # 화면/포커스 안정 대기
    time.sleep(0.5)

    if matched_lines:
        print("yes")
        pyautogui.write(";s", interval=0.05)
        pyautogui.press("space")
        pyautogui.press("backspace")
        time.sleep(1)
        pyautogui.press("enter")
        pyautogui.press("enter")
    else:
        print("no")
        pyautogui.write(";g", interval=0.05)
        pyautogui.press("space")
        pyautogui.press("backspace")
        time.sleep(1)
        pyautogui.press("enter")
        pyautogui.press("enter")


if __name__ == "__main__":
    print("Auto 무기 강화 (Ctrl + C 로 종료)")
    try:
        while True:
            detect_text_on_screen()
            time.sleep(2)  # 🔁 반복 주기 (초 단위, 필요에 따라 조절)
    except KeyboardInterrupt:
        print("종료됨")