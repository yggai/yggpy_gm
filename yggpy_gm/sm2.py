# Self-implemented minimal SM2 key generation matching JS library behavior
# No external deps. Implements finite field ops over sm2p256v1 and scalar mult.
from __future__ import annotations

import secrets
from typing import Tuple

# SM2 curve parameters (recommended curve sm2p256v1) as per GM/T 0003.5-2012
# Match JS constants in tmp/src/core/sm2/curve.ts (BigInt literals)
p = int("FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF", 16)
a = int("FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC", 16)
b = int("28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93", 16)
Gx = int("32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7", 16)
Gy = int("BC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0", 16)
n = int("FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123", 16)

O = (0, 0)  # point at infinity representation


def _mod(x: int, m: int) -> int:
    r = x % m
    return r if r >= 0 else r + m


def inv_mod(k: int, mod: int) -> int:
    # Modular inverse using extended builtin (Python 3.8+)
    return pow(_mod(k, mod), -1, mod)


def is_on_curve(P: Tuple[int, int]) -> bool:
    if P == O:
        return True
    x, y = P
    left = _mod(y * y, p)
    right = _mod(x * x * x + a * x + b, p)
    return left == right


def point_add(P: Tuple[int, int], Q: Tuple[int, int]) -> Tuple[int, int]:
    if P == O:
        return Q
    if Q == O:
        return P
    x1, y1 = P
    x2, y2 = Q
    # P + (-P) = O
    if x1 == x2 and _mod(y1 + y2, p) == 0:
        return O
    if P == Q:
        # tangent slope: (3*x1^2 + a) / (2*y1)
        num = _mod(3 * x1 * x1 + a, p)
        den = _mod(2 * y1, p)
        lam = _mod(num * inv_mod(den, p), p)
    else:
        num = _mod(y2 - y1, p)
        den = _mod(x2 - x1, p)
        lam = _mod(num * inv_mod(den, p), p)
    x3 = _mod(lam * lam - x1 - x2, p)
    y3 = _mod(lam * (x1 - x3) - y1, p)
    return (x3, y3)


def scalar_mult(k: int, P: Tuple[int, int]) -> Tuple[int, int]:
    if k % n == 0 or P == O:
        return O
    k = k % n
    result = O
    addend = P
    while k:
        if k & 1:
            result = point_add(result, addend)
        addend = point_add(addend, addend)
        k >>= 1
    return result


def gen_private_key() -> int:
    while True:
        d = secrets.randbelow(n)
        if 1 <= d <= n - 1:
            return d


def getKey() -> Tuple[str, str]:
    """Generate SM2 key pair.

    Returns (secretKey, publicKey) as hex strings; public key is uncompressed with 04 prefix.
    """
    d = gen_private_key()
    P = scalar_mult(d, (Gx, Gy))
    if P == O:
        # Extremely unlikely; regenerate
        return getKey()
    assert is_on_curve(P)
    x, y = P
    secret = f"{d:064x}"
    public = "04" + f"{x:064x}{y:064x}"
    return secret, public

