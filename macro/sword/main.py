import time
import logging
from constants import RUN_MODE, LOOP_INTERVAL
from state import MacroState
from cycle import process_cycle
from test_cycle import run_tests

logging.basicConfig(
    filename="ocr_detect.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def main():
    if RUN_MODE == "TEST":
        run_tests()
        return

    print("[안내] 자동 무기 강화 매크로 시작 (Ctrl+C 종료)")
    state = MacroState()

    try:
        while True:
            state = process_cycle(state)
            time.sleep(LOOP_INTERVAL)
    except KeyboardInterrupt:
        print("[안내] 종료됨")

if __name__ == "__main__":
    main()