# SM3 digest (port aligned with tmp/src/core/sm3/digest.ts)
from __future__ import annotations

from typing import List

MASK32 = 0xFFFFFFFF


def _rotl(x: int, n: int) -> int:
    n &= 31  # ensure rotation within 0..31 like JS
    return ((x << n) | (x >> (32 - n))) & MASK32


def _P0(x: int) -> int:
    return (x ^ _rotl(x, 9) ^ _rotl(x, 17)) & MASK32


def _P1(x: int) -> int:
    return (x ^ _rotl(x, 15) ^ _rotl(x, 23)) & MASK32

IV = [
    0x7380166F,
    0x4914B2B9,
    0x172442D7,
    0xDA8A0600,
    0xA96F30BC,
    0x163138AA,
    0xE38DEE4D,
    0xB0FB0E4E,
]


def _T(j: int) -> int:
    return 0x79CC4519 if j <= 15 else 0x7A879D8A


def _FF(x: int, y: int, z: int, j: int) -> int:
    return (x ^ y ^ z) & MASK32 if j <= 15 else ((x & y) | (x & z) | (y & z)) & MASK32


def _GG(x: int, y: int, z: int, j: int) -> int:
    return (x ^ y ^ z) & MASK32 if j <= 15 else ((x & y) | ((~x) & z)) & MASK32


def _to_uint32_be(block: bytes) -> List[int]:
    # returns 16 words (for 64-byte block), big-endian
    out = []
    for i in range(0, len(block), 4):
        w = ((block[i] << 24) | (block[i + 1] << 16) | (block[i + 2] << 8) | (block[i + 3])) & MASK32
        out.append(w)
    return out


def _from_uint32_be(words: List[int]) -> bytes:
    out = bytearray()
    for w in words:
        w &= MASK32
        out += bytes([(w >> 24) & 0xFF, (w >> 16) & 0xFF, (w >> 8) & 0xFF, w & 0xFF])
    return bytes(out)


def _compress(v: List[int], block: bytes) -> List[int]:
    w = [0] * 68
    wp = [0] * 64
    b = _to_uint32_be(block)
    for i in range(16):
        w[i] = b[i] & MASK32
    for i in range(16, 68):
        tmp = (w[i - 16] ^ w[i - 9] ^ _rotl(w[i - 3], 15)) & MASK32
        w[i] = (_P1(tmp) ^ _rotl(w[i - 13], 7) ^ w[i - 6]) & MASK32
    for i in range(64):
        wp[i] = (w[i] ^ w[i + 4]) & MASK32

    a, b1, c, d, e, f, g, h = v
    for j in range(64):
        ss1 = _rotl(((_rotl(a, 12) + e + _rotl(_T(j), j)) & MASK32), 7)
        ss2 = (ss1 ^ _rotl(a, 12)) & MASK32
        tt1 = (_FF(a, b1, c, j) + d + ss2 + wp[j]) & MASK32
        tt2 = (_GG(e, f, g, j) + h + ss1 + w[j]) & MASK32
        d = c
        c = _rotl(b1, 9)
        b1 = a
        a = tt1 & MASK32
        h = g
        g = _rotl(f, 19)
        f = e
        e = _P0(tt2)
    return [
        (v[0] ^ a) & MASK32,
        (v[1] ^ b1) & MASK32,
        (v[2] ^ c) & MASK32,
        (v[3] ^ d) & MASK32,
        (v[4] ^ e) & MASK32,
        (v[5] ^ f) & MASK32,
        (v[6] ^ g) & MASK32,
        (v[7] ^ h) & MASK32,
    ]


def _pad(msg: bytes) -> bytes:
    bit_len = (len(msg) * 8)
    # k such that len(msg)*8 + 1 + k ≡ 448 (mod 512)
    k_pad = (448 - ((len(msg) * 8 + 1) % 512) + 512) % 512
    pad_len = 1 + (k_pad // 8) + 8
    out = bytearray(len(msg) + pad_len)
    out[: len(msg)] = msg
    out[len(msg)] = 0x80
    # 64-bit big-endian length
    len_offset = len(out) - 8
    tmp = bit_len
    for i in range(7, -1, -1):
        out[len_offset + i] = tmp & 0xFF
        tmp >>= 8
    return bytes(out)


def digest(data: bytes) -> bytes:
    v = IV.copy()
    m = _pad(data)
    for i in range(0, len(m), 64):
        v = _compress(v, m[i : i + 64])
    return _from_uint32_be(v)


def digest_hex(data: bytes) -> str:
    return digest(data).hex()

