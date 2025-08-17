import os
import sys
import subprocess
from setuptools import setup, find_packages


def _obfuscate_if_needed():
    """
    If env YGG_OBFUSCATE=1, run PyArmor to obfuscate package into build/obf
    and return packaging configuration pointing to obfuscated output.
    """
    if os.environ.get("YGG_OBFUSCATE") != "1":
        return {
            "packages": find_packages(exclude=("tests", "examples")),
            "package_dir": {},
            "include_package_data": False,
            "package_data": {},
        }

    out_dir = os.path.join("build", "obf")
    src_pkg = "yggpy_gm"

    try:
        cmd = [sys.executable, "-m", "pyarmor", "obfuscate", "-r", "-O", out_dir, src_pkg]
        print("[setup] Running:", " ".join(cmd))
        subprocess.check_call(cmd)
    except FileNotFoundError:
        raise SystemExit("PyArmor is not installed. Please `pip install pyarmor` and retry.")
    except subprocess.CalledProcessError as e:
        raise SystemExit(f"PyArmor obfuscation failed with exit code {e.returncode}.")

    # Find packages from obfuscated output; include pytransform runtime
    packages = find_packages(where=out_dir, include=["yggpy_gm*", "pytransform*"])
    package_dir = {"": out_dir}

    # Include pyarmor runtime binaries in wheel
    package_data = {
        "pytransform": [
            "*",
            "platforms/*/*",
            "platforms/*/*/*",
        ]
    }

    return {
        "packages": packages,
        "package_dir": package_dir,
        "include_package_data": True,
        "package_data": package_data,
    }


pkg_cfg = _obfuscate_if_needed()

setup(
    name="yggpy_gm",
    version="0.0.1",
    description="Python SM2/SM3/SM4 utils aligned with yggjs_gm",
    author="",
    packages=pkg_cfg["packages"],
    package_dir=pkg_cfg["package_dir"],
    include_package_data=pkg_cfg["include_package_data"],
    package_data=pkg_cfg["package_data"],
    python_requires=">=3.8",
    install_requires=[
        "gmssl>=3.2.1",
    ],
)
