import yggpy_gm as gggm

secretKey, publicKey  = gggm.getSm2Key()
print('私钥：', secretKey)
print('公钥：', publicKey)