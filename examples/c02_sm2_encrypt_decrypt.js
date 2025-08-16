import gggm from 'yggjs-gm';

// 生成公钥和私钥
const { privateKey, publicKey } = gggm.getKey();
console.log('私钥：', privateKey);
console.log('公钥：', publicKey);

// 使用公钥进行加密
const originStr = 'zhangdapeng520';
const encryptStr = gggm.sm2Encrypt(publicKey, originStr);
console.log('加密后的字符串：', encryptStr);

// 使用私钥进行解密
const decryptStr = gggm.sm2Decrypt(privateKey, encryptStr);
console.log('解密后的字符串：', decryptStr);

// 解密之后的必须和原始的相同
console.log('原始字符串和解密后的字符串是否相同：', originStr === decryptStr);
