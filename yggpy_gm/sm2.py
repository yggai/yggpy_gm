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
