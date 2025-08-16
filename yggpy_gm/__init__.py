"""yggpy_gm: Python SM2 utilities matching yggjs_gm behavior.

Public API:
- getKey() -> (secretKey:str, publicKey:str)
- sm2Encrypt(public_key_hex: str, plaintext_utf8: str) -> ciphertext_hex: str
- sm2Decrypt(private_key_hex: str, ciphertext_hex: str) -> plaintext_utf8: str

Formats:
- secretKey: 64-hex lowercase, without 0x
- publicKey: uncompressed point, '04' + x(64-hex) + y(64-hex)
- Ciphertext: hex of C1(04||x||y)||C2||C3 per tmp/src implementation
"""
from .sm2 import getKey
from .sm2_encrypt import sm2Encrypt, sm2Decrypt

__all__ = ["getKey", "sm2Encrypt", "sm2Decrypt"]

