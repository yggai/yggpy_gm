from setuptools import setup, find_packages

setup(
    name="yggpy_gm",
    version="0.0.1",
    description="Python SM2/SM3/SM4 utils aligned with yggjs_gm",
    author="",
    packages=find_packages(exclude=("tests", "examples")),
    python_requires=">=3.8",
)

