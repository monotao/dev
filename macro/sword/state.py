from dataclasses import dataclass
from typing import Optional
from constants import MODE_ENHANCE
# from constants import MODE_SEED

@dataclass
class MacroState:
    paused: bool = False
    mode: str = MODE_ENHANCE
    target: int = 10
    # mode: str = MODE_SEED
    # target: int = 8
    loop: int = 1

    last_level: Optional[int] = None
    prev_hidden_item: Optional[str] = None