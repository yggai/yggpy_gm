import os
import sys
# 确保优先导入当前工作区的包实现（而不是已安装的旧版本）
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import binascii
import re
import pytest

from yggpy_gm.sm2 import sm2Decrypt

# 固定测试向量（来自 examples/c03_js_encrypt_py_decrypt.py）
PRIVATE_KEY = "9db951680065cb605e126dae8738e5bdc656d3be8d437ddcfdc945eff17ec936"
PUBLIC_KEY = (
    "04"
    "a95d48d4b039d795723d47843ce293991940e64b742630354647ad59208721"
    "7742e3642d1b3b08030d2d359331b581c6d780fe41a3780c26e92fe5b9b747bfb6"
)
PLAINTEXT = "zhangdapeng520"
JS_CIPHERTEXT = (
    "1adb29f669a6cfe747e10d0b222b17d3bb36338f292300b724ab9f85be647ffc"
    "178a83954976f64f7b040d274072d039a64861ea21e03917c1032fb705fab66f"
    "f78784bb75c2069316529f4f511709f9fc63cc757b4915c4bb62217267645b2e"
    "c10d151c27e9e79e1358d10c651e"
)


def is_hex(s: str) -> bool:
    return bool(re.fullmatch(r"[0-9a-f]+", s))


def test_sm2_decrypt_js_ciphertext_matches_plaintext():
    # 已知 JS 的密文能被 Python 成功解密
    out = sm2Decrypt(PRIVATE_KEY, PUBLIC_KEY, JS_CIPHERTEXT)
    assert out == PLAINTEXT


def test_sm2_encrypt_then_decrypt_roundtrip():
    # 延迟导入，便于在实现 sm2Encrypt 前先观察到测试失败（TDD）
    from yggpy_gm.sm2 import sm2Encrypt

    cipher_hex = sm2Encrypt(PUBLIC_KEY, PLAINTEXT)

    # 基本形态检查：十六进制、长度大于明文且不等于明文
    assert isinstance(cipher_hex, str)
    assert is_hex(cipher_hex)
    assert len(cipher_hex) > len(PLAINTEXT)

    # 能被 sm2Decrypt 还原
    restored = sm2Decrypt(PRIVATE_KEY, PUBLIC_KEY, cipher_hex)
    assert restored == PLAINTEXT

