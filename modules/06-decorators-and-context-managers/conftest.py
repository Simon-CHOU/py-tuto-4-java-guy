import os
import sys
from pathlib import Path

_target = Path(__file__).resolve().parent / os.environ.get("PRACTICE_TARGET", "complete")
sys.path.insert(0, str(_target))
