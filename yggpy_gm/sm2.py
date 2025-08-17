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
