import base64
from Crypto.Cipher import AES
import json
# 密钥（key）, 密斯偏移量（iv） CBC模式加密

def AES_Encrypt(key,vi,data):
    vi = vi
    pad = lambda s: s + (16 - len(s)%16) * chr(16 - len(s)%16)
    data = pad(data)
    # 字符串补位
    cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, vi.encode('utf8'))
    encryptedbytes = cipher.encrypt(data.encode('utf8'))
    # 加密后得到的是bytes类型的数据
    encodestrs = base64.b64encode(encryptedbytes)
    # 使用Base64进行编码,返回byte字符串
    enctext = encodestrs.decode('utf8')
    # 对byte字符串按utf-8进行解码
    return enctext


def AES_Decrypt(key,vi,data):
    vi = vi
    data = data.encode('utf8')
    encodebytes = base64.decodebytes(data)
    # 将加密数据转换位bytes类型数据
    cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, vi.encode('utf8'))
    text_decrypted = cipher.decrypt(encodebytes)
    unpad = lambda s: s[0:-s[-1]]
    text_decrypted = unpad(text_decrypted)
    # 去补位
    text_decrypted = text_decrypted.decode('utf8')
    return text_decrypted



if __name__ =='__main__':
    key = '1234567890abcdef'
    vi = '1234567890abcdef'
    data = {"OperatorID":"MA5DA0053","OperatorSecret":"abcdef1234567890"}
    #data = {"StationIDs":"000000088003"}
    data = json.dumps(data)
    enctext = AES_Encrypt(key,vi, data)
    print(enctext)
    data1="BmuQPtmtMfSqKqTPqiWVUAYFBN6VGfUH7INq04il+WN/cUIZr3iVlfJoY52ESRFUFDFUEWDloc6BqN8VSLMQug=="
    text_decrypted = AES_Decrypt(key,vi,data1)
    print(text_decrypted)