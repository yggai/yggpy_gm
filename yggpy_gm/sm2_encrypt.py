# SM2 encrypt/decrypt (C1C2C3) aligned with tmp/src implementation
from __future__ import annotations

from typing import Tuple

from .sm2 import Gx, Gy, n, scalar_mult
from .sm3 import digest


def _bigint_to_32bytes(x: int) -> bytes:
    h = f"{x:064x}"
    return bytes.fromhex(h)


def _bytes_to_bigint(b: bytes) -> int:
    x = 0
    for v in b:
        x = (x << 8) | v
    return x


def _kdf_z(x2y2: bytes, klen: int) -> bytes:
    # Same construction as tmp/src/core/sm2/encrypt.ts & decrypt.ts
    # concatenate SM3(x2y2 || ct) for ct = 1..ceil(klen/32)
    out = bytearray()
    ct_max = (klen + 31) // 32
    for ct in range(1, ct_max + 1):
        counter = bytes([0, 0, 0, ct & 0xFF])
        out += digest(x2y2 + counter)
    return bytes(out[:klen])


def sm2Encrypt(public_key_hex: str, plaintext_utf8: str) -> str:
    # Parse uncompressed public key hex: may be '04' + 64 + 64 or just 128 hex (without 04)
    h = public_key_hex.strip().lower()
    if h.startswith("0x"):
        h = h[2:]
    if h.startswith("04"):
        h = h[2:]
    if len(h) != 128:
        raise ValueError("无效的公钥长度")
    x = int(h[:64], 16)
    y = int(h[64:], 16)

    # Random k: we mirror JS behavior by using Python's secrets via sm2.gen_private_key-like range
    import secrets

    k = 0
    while k == 0:
        k = secrets.randbelow(n)
        if not (1 <= k <= n - 1):
            k = 0

    # C1 = kG
    C1x, C1y = scalar_mult(k, (Gx, Gy))
    # (x2, y2) = kP
    x2, y2 = scalar_mult(k, (x, y))

    x2b = _bigint_to_32bytes(x2)
    y2b = _bigint_to_32bytes(y2)

    pt = plaintext_utf8.encode("utf-8")
    z = x2b + y2b
    t = _kdf_z(z, len(pt))
    C2 = bytes([pt[i] ^ t[i] for i in range(len(pt))])

    C3 = digest(x2b + pt + y2b)

    # Output C1||C2||C3; C1 uncompressed 04||x||y
    C1 = b"\x04" + _bigint_to_32bytes(C1x) + _bigint_to_32bytes(C1y)
    out = C1 + C2 + C3
    return out.hex()


def sm2Decrypt(private_key_hex: str, ciphertext_hex: str) -> str:
    h = ciphertext_hex.strip().lower()
    if h.startswith("0x"):
        h = h[2:]
    data = bytes.fromhex(h)
    if len(data) < 1 + 32 + 32 + 32:
        raise ValueError("密文长度无效")
    if data[0] != 0x04:
        raise ValueError("仅支持未压缩点")

    x1 = _bytes_to_bigint(data[1:33])
    y1 = _bytes_to_bigint(data[33:65])
    C1 = (x1, y1)

    C3 = data[-32:]
    C2 = data[65:-32]

    d = int(private_key_hex.strip().lower().removeprefix("0x"), 16)

    x2, y2 = scalar_mult(d, C1)
    x2b = _bigint_to_32bytes(x2)
    y2b = _bigint_to_32bytes(y2)

    z = x2b + y2b
    t = _kdf_z(z, len(C2))
    M = bytes([C2[i] ^ t[i] for i in range(len(C2))])

    u = digest(x2b + M + y2b)
    if u != C3:
        raise ValueError("C3 校验失败")

    return M.decode("utf-8")

