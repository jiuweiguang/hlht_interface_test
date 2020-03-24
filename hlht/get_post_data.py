from tool.getExcelData import getExcelData
from tool.AES import AES_Encrypt
from tool.md5 import encryptHex2Upper
import time
def get_post_data():
    data = getExcelData().getData()
    heards = {"Content-Type": "application/json"}
    list_post_data = []
    for i in range(0,len(data)):
        test_id = data[i]["test_id"]
        test_url = data[i]["test_url"]
        test_addr = data[i]["test_addr"]
        test_data = data[i]["test_data"]
        test_opertorid = str(data[i]["test_opertorid"])
        test_operatorsecret = data[i]["test_operatorsecret"]
        test_datasecret = data[i]["test_datasecret"]
        test_datasecretiv = data[i]["test_datasecretiv"]
        test_sigsecret = data[i]["test_sigsecret"]
        address = test_url + test_addr
        if data[i]["test_ency"] == 'True':
            data_encrypt = AES_Encrypt(key=test_datasecret,vi=test_datasecretiv,data=test_data)
            timeStamp = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
            seq = "0001"
            sig_data = test_opertorid + data_encrypt + timeStamp + seq
            sig = encryptHex2Upper(key=test_sigsecret,data=sig_data)
            post_data = {"OperatorID":test_opertorid,
                                  "Data":data_encrypt,
                                  "TimeStamp":timeStamp,
                                  "Seq":seq,
                                  "Sig":sig
                                  }
            return_data = {"id":test_id,
                           "address":address,
                           "url":test_url,
                           "postdata":post_data,
                           "test_addr":test_addr,
                           "datasecret":test_datasecret,
                           "datasecretiv":test_datasecretiv,
                           "operatorsecret":test_operatorsecret,
                           "opertorid":test_opertorid,
                           "sigsecret":test_sigsecret}
            list_post_data.append(return_data)
        elif data[i]["test_ency"] == 'False':
            post_data = eval(test_data)
            return_data = {"id":test_id,
                           "address":address,
                           "url":test_url,
                           "postdata":post_data,
                           "test_addr":test_addr,
                           "datasecret":test_datasecret,
                           "datasecretiv":test_datasecretiv,
                           "operatorsecret":test_operatorsecret,
                           "opertorid":test_opertorid,
                           "sigsecret":test_sigsecret}
            list_post_data.append(return_data)
    return list_post_data
        # status_code,result = post(header=heards,address=address,data=post_data)
        # result_data = result['Data']
        # result_data_decrypt  = AES_Decrypt(key=test_datasecret,vi=test_datasecretiv,data=result_data)
        # print('status_code:%s\n'%status_code + 'token result:%s\n'%result + '解密数据%s\n'%result_data_decrypt)