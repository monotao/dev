import pyautogui
import pytesseract
import cv2
import numpy as np

# def capture_and_ocr(lang: str, config: str) -> list[str]:
#     screenshot = pyautogui.screenshot()
#     img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     text = pytesseract.image_to_string(gray, lang=lang, config=config)
#     return [line.strip() for line in text.splitlines() if line.strip()]

def capture_and_ocr_roi(
    roi: tuple[int, int, int, int],
    *,
    lang: str,
    config: str,
) -> list[str]:
    screenshot = pyautogui.screenshot(region=roi)
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    text = pytesseract.image_to_string(gray, lang=lang, config=config)
    return [line.strip() for line in text.splitlines() if line.strip()]