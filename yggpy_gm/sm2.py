from gmssl import sm2
import binascii


def sm2Decrypt(privateKey, publicKey, text):
    """
    基于sm2的密码解密
    """
    sm2_crypt = sm2.CryptSM2(
        private_key=privateKey,
        public_key=publicKey,
        ecc_table=sm2.default_ecc_table,
    )
    cipher_bytes = binascii.unhexlify(text)
    return sm2_crypt.decrypt(cipher_bytes).decode("utf-8")



def sm2Encrypt(publicKey, text: str) -> str:
    """
    基于SM2的公钥加密
    - 输入: publicKey 为未压缩公钥(十六进制, 以04开头), text 为待加密明文字符串
    - 输出: 密文的十六进制字符串
    """
    sm2_crypt = sm2.CryptSM2(
        private_key="",
        public_key=publicKey,
        ecc_table=sm2.default_ecc_table,
    )
    if isinstance(text, str):
        data = text.encode("utf-8")
    else:
        # 容错: 如果不小心传了 bytes
        data = bytes(text)
    cipher_bytes = sm2_crypt.encrypt(data)
    return binascii.hexlify(cipher_bytes).decode("utf-8")



def getSm2Key():
    """
    生成一对 SM2 密钥 (私钥十六进制64位, 公钥未压缩十六进制130位，以04开头)
    :return: (private_key_hex, public_key_hex)
    """
    from gmssl import func as gmfunc

    ecc_table = sm2.default_ecc_table
    n = int(ecc_table["n"], 16)

    # 使用 gmssl 的随机函数生成 64 位十六进制私钥，保证在 [1, n-1]
    while True:
        private_key = gmfunc.random_hex(64)
        d = int(private_key, 16)
        if 1 <= d < n:
            break

    # 通过标量乘法计算未压缩公钥 (x||y)
    sm2_crypt = sm2.CryptSM2(private_key=private_key, public_key="", ecc_table=ecc_table)
    public_xy = sm2_crypt._kg(int(private_key, 16), ecc_table["g"])  # 128 hex chars

    public_key = "04" + public_xy  # 未压缩前缀
    return private_key, public_key
