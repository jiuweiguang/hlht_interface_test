import hmac
import hashlib


def encryptHex2Upper(key,data):#MD5加密，输出消息密文
    ekey=key
    ekey=ekey.encode(encoding='utf-8')
    to_enc=data
    to_enc = to_enc.encode(encoding='utf-8')
    enc_res = hmac.new(ekey,to_enc,hashlib.md5).hexdigest().upper()
    return enc_res

if __name__=='__main__':
    key = 'abcdef1234567890'
    data = 'MA5DA0053Yh8Vi+8xpJ5b9CbsMY4wkeVIh81VtKvVFcLZxaI9+hNkaSyA1sQN0SiD2TLRdp8gHhCAMFp4ky2OhhjtqXJ9zINP3gy7Ahytmyi73LeTUZw=202003051547363113'
    result = encryptHex2Upper(key,data)
    print(result)