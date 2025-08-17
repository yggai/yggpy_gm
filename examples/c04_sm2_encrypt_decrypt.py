import yggpy_gm as gggm

privateKey = "9db951680065cb605e126dae8738e5bdc656d3be8d437ddcfdc945eff17ec936"
publicKey = "04a95d48d4b039d795723d47843ce293991940e64b742630354647ad592087217742e3642d1b3b08030d2d359331b581c6d780fe41a3780c26e92fe5b9b747bfb6"
text = "zhangdapeng520"

# 使用Python进行加密
encryptStr = gggm.sm2Encrypt(publicKey, text)
print("加密后的字符串：", encryptStr)

# 使用Python进行解密
decryptStr = gggm.sm2Decrypt(privateKey, publicKey, encryptStr)
print('解密后的字符串：', decryptStr)
print('解密后的字符串与JavaScript是否相等：', decryptStr == text)