import pyautogui
import pyperclip
import time
from constants import TYPE_INTERVAL, ENTER_DELAY

def send_command(cmd: str):
    pyautogui.write(cmd, interval=TYPE_INTERVAL)
    pyautogui.press("space")
    pyautogui.press("backspace")
    time.sleep(ENTER_DELAY)
    pyautogui.press("enter")
    pyautogui.press("enter")

def send_command_korean(cmd: str):
    pyperclip.copy(cmd)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("space")
    pyautogui.press("backspace")
    time.sleep(ENTER_DELAY)
    pyautogui.press("enter")
    pyautogui.press("enter")