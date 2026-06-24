import os
import sys
from pathlib import Path

print('cwd:', os.getcwd())
print('sys.executable:', sys.executable)
print('__file__:', Path(__file__).resolve())
print('script dir:', Path(__file__).resolve().parent)
print('argv:', sys.argv)
