macro/
 ├─ sword/
 │   ├─ constants.py
 │   ├─ state.py
 │   ├─ ocr.py
 │   ├─ input.py
 │   ├─ parser.py
 │   ├─ mode_engine.py
 │   ├─ cycle.py
 │   ├─ test_cycle.py
 │   ├─ main.py
 ├─ tests/
 │   ├─ conftest.py
 │   ├─ test_parser.py
 │   ├─ test_mode_engine.py
 │   └─ test_cycle.py

## Windows
# VMWare 설치
# Anaconda 설치
https://www.anaconda.com/download

# 라이브러리 설치
https://github.com/UB-Mannheim/tesseract/wiki
설치경로: C:\Program Files\Tesseract-OCR\

# 환경설정
<PowerShell>
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

<시스템 속성>
환변 변수 클릭 -> 시스템 변수의 Path를 선택하고 편집 -> 새로 만들기 -> 다음의 내용을 복사 붙여 넣기 후 확인 C:\Program Files\Tesseract-OCR\ -> 확인

# 가상환경 설정
conda init powershell
conda create -n sword python=3.12.1
conda activate sword

# 라이브러리 설치
pip install pyautogui pywin32 pillow pytesseract opencv-python numpy

# 좌표값 설정
아래와 같이 좌표값 구하는 코드 수행 후 결과 값을 constants.py의 GAME_ROI에 붙여넣기
python get_roi.py

# 매크로 실행
아래의 같이 코드 수행 후 대상이 되는 카카오톡 대화창 입력 칸에 커서 놓고 클릭하기
python main.py


## Mac
# brew 설치
https://brew.sh/
brew install python

# 환경설정
vi ~/.zshrc
source ~/.zshrc
export PATH=/opt/homebrew/bin:$PATH

# 폴더생성 및 이동
mkdir macro
cd macro


# 가상환경 설정
python -m venv sword
source sword/bin/activate

# 라이브러리 설치
pip install bleak pyautogui pytesseract opencv-python pillow pyperclip
brew install tesseract
brew install tesseract-lang

# 텍스트 대치 설정
시스템 설정 -> 키보드 -> 텍스트 입력의 텍스트 대치 클릭 -> + 버튼 누르고 ;g는 /강, ;s는 /판 으로 설정

# 일부코드 수정
mode_engine.py
위 코드에서 아래의 코드를 다음의 코드로 대치하기
send_command_korean("/판") -> send_command(";s")
send_command_korean("/강") -> send_command(";g")

# 좌표값 설정
아래와 같이 좌표값 구하는 코드 수행 후 결과 값을 constants.py의 GAME_ROI에 붙여넣기
python get_roi.py

# 매크로 실행
아래의 같이 코드 수행 후 대상이 되는 카카오톡 대화창 입력 칸에 커서 놓고 클릭하기
python main.py