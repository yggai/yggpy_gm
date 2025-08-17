import os

os.system("python setup.py bdist_wheel")
os.system("pip install dist/yggpy_gm-0.0.1-py3-none-any.whl")