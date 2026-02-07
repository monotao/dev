from cycle import process_cycle_core
from state import MacroState
from constants import MODE_ENHANCE

def run_tests():
    scenarios = [
        (["무기 강화 [+9]"], ["target 10"]),
        (["무기 강화 [+10]"], []),
        (["광선검"], ["hidden"]),
    ]

    state = MacroState(
        paused=False,
        mode=MODE_ENHANCE,
        target=10,
        loop=1,
    )

    for i, (g, c) in enumerate(scenarios, 1):
        print(f"\n--- cycle {i} ---")
        state = process_cycle_core(state, g, c)
        print(state)