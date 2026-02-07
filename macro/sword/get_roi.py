import pyautogui
import time

print("5초 후 시작합니다. 마우스를 ROI 좌상단에 올려두세요...")
time.sleep(5)

x1, y1 = pyautogui.position()
print(f"TOP-LEFT  : ({x1}, {y1})")

print("5초 후 우하단 좌표를 찍습니다. 마우스를 이동하세요...")
time.sleep(5)

x2, y2 = pyautogui.position()
print(f"BOTTOM-RIGHT: ({x2}, {y2})")

w = x2 - x1
h = y2 - y1

print("\n=== ROI RESULT ===")
print(f"ROI = ({x1}, {y1}, {w}, {h})")