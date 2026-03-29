import os
import time
import pytest


OPERA_GX_PATH = os.path.join(
    os.path.expanduser("~"),
    "AppData", "Local", "Programs", "Opera GX", "opera.exe"
)

os.makedirs("reports", exist_ok = True)

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "executable_path": OPERA_GX_PATH,
        "slow_mo": 1000,
    }

@pytest.fixture(autouse=True)
def pause_after_tests():
    yield
    time.sleep(3)

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": None,
    }
