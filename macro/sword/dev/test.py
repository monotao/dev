import pyautogui
import pytesseract
import cv2
import numpy as np
import time
import logging
import re

# ==================================================
# 히든 무기 키워드
# ==================================================
HIDDEN_KEYWORDS = [
    "광선검", "지킨 검", "심판검", "불의 검", "빛의 검",
    "슬리퍼", "샌들", "신발",
    "꽃다발", "다발", "에덴동산", "오르페우스",
    "우산", "천막", "방패", "아이기스", "아이기스 원형",
    "젓가락", "비도", "반고가 세상",
    "소시지", "핫도그",
    "칫솔", "치솔", "칫소", "치소", "치실", "털이", "곰팡이", "치약", "포자", "치아", "이빨",
    "빗자루", "주전자", "단소", "브레드",
    "채찍", "붉은 끈", "붉은 꼬리", "고삐", "붉은 기수", "핏빛 날개", "가르는 꼬리", "붉은 혜성", "삼킨 적토마", "말의 궤적", "붉은 짐승",
    "기타", "유발자", "앰프", "디스토션", "피드백", "악기", "광란의 지배자", "레퀴엠", "심연 현", "진짜 리라", "계약서", "뇌명 제우스", "초끈", "시발점", "공명 주파수", "벤딩", "지휘자",
    "하드", "3초 룰", "프리즈", "액체질소", "와사비", "녹차", "초콜릿", "바닐라", "쿠키", "융단폭격", "민트초코", "파이퍼", "엑스칼리", "설탕", "밀크", "아이스바", "파르페"
]

test_lines = [
    "망치",
    "털이"
]

def detect_hidden_weapon(lines: list[str]) -> str | None:
    for line in lines:
        for kw in HIDDEN_KEYWORDS:
            if kw in line:
                print(f"[MATCH] line='{line}' → keyword='{kw}'")
                return kw
    print("[NO MATCH]")
    return None


result = detect_hidden_weapon(test_lines)
print("result =", result)