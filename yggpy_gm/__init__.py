"""yggpy_gm: Python SM2 utilities matching yggjs_gm behavior.

Public API:
- getKey() -> (secretKey:str, publicKey:str)

Formats:
- secretKey: 64-hex lowercase, without 0x
- publicKey: uncompressed point, '04' + x(64-hex) + y(64-hex)
"""
from .sm2 import getKey

__all__ = ["getKey"]

