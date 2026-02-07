import re
import logging
from constants import HIDDEN_KEYWORDS

def extract_enhance_level(lines: list[str]) -> int | None:
    for line in lines:
        m = re.search(r"\[\+(\d+)", line)
        if m:
            value = int(m.group(1))
            if value > 20:
                logging.info(f"[안내] 강화 수치 OCR 이상치 무시: {value}")
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
        m = re.search(r"(enhance|sell|hidden|seed)", line)
        if m:
            return m.group(1), line
    return current_mode, None

def parse_levels(cmd_lines, target):
    for line in cmd_lines:
        m = re.search(r"target\s*\+?\s*(\d+)", line)
        if m:
            new = int(m.group(1))
            if new != target:
                logging.info(f"[안내] 목표변경 {target} → {new}")
            target = new
    return target

def detect_control(cmd_lines, paused):
    if any("stop" in line for line in cmd_lines):
        return True
    if any("start" in line for line in cmd_lines):
        return False
    return paused

def should_enhance_hidden(level, safe_level, target):
    if level == 0:
        return True
    if safe_level <= target and level >= safe_level:
        return True
    return False