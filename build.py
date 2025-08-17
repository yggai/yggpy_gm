import os

os.system("python setup.py sdist")
os.system("pip install dist/yggpy_gm-0.0.1.tar.gz")