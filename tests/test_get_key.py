import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import re
import pytest

from yggpy_gm.sm2 import sm2Encrypt, sm2Decrypt

HEX_RE = re.compile(r"^[0-9a-f]+$")


def test_get_key_returns_valid_hex_and_roundtrip():
    # TDD: 先导入包根方法（当前应失败）
    from yggpy_gm import getSm2Key

    priv, pub = getSm2Key()

    # 基本格式校验
    assert isinstance(priv, str) and isinstance(pub, str)
    assert len(priv) == 64 and HEX_RE.fullmatch(priv)
    assert len(pub) == 130 and pub.startswith("04") and HEX_RE.fullmatch(pub)

    # 回环验证：使用生成的密钥进行加解密
    msg = "hello-sm2"
    c = sm2Encrypt(pub, msg)
    out = sm2Decrypt(priv, pub, c)
    assert out == msg

