import yggpy_gm as gggm


def test_sm2_encrypt_decrypt_roundtrip():
    sk, pk = gggm.getKey()
    pt = "zhangdapeng520"
    ct = gggm.sm2Encrypt(pk, pt)
    assert isinstance(ct, str) and len(ct) > 0
    dec = gggm.sm2Decrypt(sk, ct)
    assert dec == pt

