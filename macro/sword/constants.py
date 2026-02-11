# 실행 모드
RUN_MODE = "LIVE"  # or "TEST"

# ROI
GAME_ROI = (94, 272, 676, 478)
CMD_ROI = (662, 212, 100, 536)

# OCR
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
)

# MODE
MODE_ENHANCE = "enhance"
MODE_SELL    = "sell"
MODE_HIDDEN  = "hidden"
MODE_SEED    = "seed"

MODE_LABEL = {
    MODE_ENHANCE: "강화모드",
    MODE_SELL:    "판매모드",
    MODE_HIDDEN:  "히든모드",
    MODE_SEED:    "시드모드",
}

MODE_CONFIG = {
    MODE_ENHANCE: dict(needs_hidden=False, auto_sell=False, auto_pause=True),
    MODE_SELL:    dict(needs_hidden=False, auto_sell=True,  auto_pause=False),
    MODE_HIDDEN:  dict(needs_hidden=True,  auto_sell=False, auto_pause=True),
    MODE_SEED:    dict(needs_hidden=True,  auto_sell=True,  auto_pause=False),
}

# Hidden keywords
HIDDEN_KEYWORDS = [
    "광선검", "지킨 검", "심판검", "불의 검", "빛의 검",
    "슬리퍼", "샌들", "신발",
    "꽃다발", "다발", "에덴동산", "오르페우스",
    "우산", "천막", "방패", "아이기스 원형", "아이기스",
    "젓가락", "비도", "반고가 세상",
    "소시지", "핫도그",
    "칫솔", "치솔", "칫소", "치소", "치실", "털이", "곰팡이", "치약", "포자", "치아", "이빨",
    "기타", "유발자", "앰프", "디스토션", "피드백", "영혼을 켜는 악기", "광란의 지배자", "레퀴엠", "심연 현", "진짜 리라", "계약서", "뇌명 제우스", "초끈", "빅뱅의 시발점", "공명 주파수", "벤딩", "지휘자", "적막 소리의 종언",
    "하드", "3초 룰", "프리즈", "액체질소", "와사비", "녹차", "초콜릿", "바닐라", "쿠키", "융단폭격", "민트초코", "파이퍼", "엑스칼리", "설탕", "밀크", "아이스바", "파르페",
    "채찍", "붉은 끈", "붉은 꼬리", "고삐", "붉은 기수", "핏빛 날개", "가르는 꼬리", "붉은 혜성", "삼킨 적토마", "말의 궤적", "붉은 짐승",
    "빗자루",
    "주전자",
    "단소",
    "브레드",
    "화살",
    "윷"
]

# Timing
TYPE_INTERVAL = 0.15
FOCUS_DELAY   = 0.2
ENTER_DELAY   = 0.15
LOOP_INTERVAL = 3