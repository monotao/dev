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

#라이브러리 설치
pip install pyautogui pywin32 pillow pytesseract opencv-python numpy


## Mac
https://brew.sh/

brew install python

vi ~/.zshrc
source ~/.zshrc
export PATH=/opt/homebrew/bin:$PATH

mkdir macro
cd macro

python -m venv sword
source sword/bin/activate

pip install bleak pyautogui pytesseract opencv-python pillow pyperclip
brew install tesseract
brew install tesseract-lang