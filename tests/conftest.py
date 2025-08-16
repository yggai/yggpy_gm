import os, sys
# Ensure the repository root is on sys.path so 'import yggpy_gm' works without install
ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

