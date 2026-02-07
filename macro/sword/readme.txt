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