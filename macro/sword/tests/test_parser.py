from parser import (
    extract_enhance_level,
    detect_hidden_weapon,
    parse_levels,
)

def test_extract_enhance_level():
    lines = ["무기 강화 [+9]"]
    assert extract_enhance_level(lines) == 9

def test_extract_enhance_level_overflow():
    lines = ["무기 강화 [+99]"]
    assert extract_enhance_level(lines) is None

def test_detect_hidden_weapon():
    lines = ["광선검"]
    assert detect_hidden_weapon(lines) == "광선검"

def test_parse_levels_change():
    cmd = ["target 12"]
    assert parse_levels(cmd, 10) == 12