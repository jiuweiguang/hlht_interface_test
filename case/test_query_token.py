import unittest
import os
from common.HTMLTestRunner_PY3 import HTMLTestRunner
import time,ddt
from hlht.get_post_data import get_post_data
from hlht.post_interface import post_interface
from multiprocessing.dummy import Pool as ThreadPool

# @ddt.ddt
class query_token(unittest.TestCase):
    data = get_post_data()

    # @ddt.data(*data)
    def test_one_equation(self):
        # print("测试用例：%s:"%self.data['id'])
        self.args_p = []

        for i in self.data:
            self.excl_data = {
                "id": "",
                "address": "",
                "postdata": "",
                "test_addr": "",
                "datasecret": "",
                "datasecretiv": "",
                "operatorsecret": "",
                "opertorid": "",
                "url": "",
                "sigsecret": ""
            }
            self.excl_data["id"] = i['id']
            self.excl_data["address"] = i['address']
            self.excl_data["postdata"] = i['postdata']
            self.excl_data["test_addr"] = i['test_addr']
            self.excl_data["datasecret"] = i['datasecret']
            self.excl_data["datasecretiv"] = i['datasecretiv']
            self.excl_data["operatorsecret"] = i['operatorsecret']
            self.excl_data["opertorid"] = str(i['opertorid'])
            self.excl_data["url"] = i['url']
            self.excl_data["sigsecret"] = i['sigsecret']
            self.args_p.append(self.excl_data)
        thread_pool=ThreadPool(1)
        thread_pool.map(post_interface,self.args_p)
        thread_pool.close()
        thread_pool.join()
        # post_interface(test_id=data['id'],
        #                address=data['address'],
        #                url=data['url'],
        #                addr=data['test_addr'],
        #                data=data['postdata'],
        #                datasecret=data['datasecret'],
        #                datasecretiv=data['datasecretiv'],
        #                operatorsecret=data['operatorsecret'],
        #                opertorid=data['opertorid'],
        #                sigsecret=data['sigsecret'])
    # data = getExcelData().getData()
    # heards = {"Content-Type":"application/json"}
    # def test_query_token(self):
    #     for i in range(0,len(self.data)):
    #         self.test_url = self.data[i]["test_url"]
    #         self.test_addr = self.data[i]["test_addr"]
    #         self.test_data = self.data[i]["test_data"]
    #         self.test_opertorid = self.data[i]["test_opertorid"]
    #         self.test_operatorsecret = self.data[i]["test_operatorsecret"]
    #         self.test_datasecret = self.data[i]["test_datasecret"]
    #         self.test_datasecretiv = self.data[i]["test_datasecretiv"]
    #         self.test_sigsecret = self.data[i]["test_sigsecret"]
    #         self.address = self.test_url + self.test_addr
    #         self.data_encrypt = AES_Encrypt(key=self.test_datasecret,vi=self.test_datasecretiv,data=self.test_data)
    #         self.timeStamp = time.strftime("%Y%m%d%H%M", time.localtime(time.time()))
    #         self.seq = "0001"
    #         self.sig_data = self.test_opertorid + self.data_encrypt + self.timeStamp + self.seq
    #         self.sig = encryptHex2Upper(key=self.test_sigsecret,data=self.sig_data)
    #         self.post_data = {"OperatorID":self.test_opertorid,
    #                           "Data":self.data_encrypt,
    #                           "TimeStamp":self.timeStamp,
    #                           "Seq":self.seq,
    #                           "Sig":self.sig
    #                           }
    #         self.status_code,self.result = post(header=self.heards,address=self.address,data=self.post_data)
    #         self.result_data = self.result['Data']
    #         self.result_data_decrypt  = AES_Decrypt(key=self.test_datasecret,vi=self.test_datasecretiv,data=self.result_data)
    #         print('status_code:%s\n'%self.status_code + 'token result:%s\n'%self.result + '解密数据%s\n'%self.result_data_decrypt)


if __name__ == '__main__':
    run_time = time.strftime('%Y-%m-%d_%H_%M_%S', time.localtime(time.time()))

    fp = open(os.getcwd()+"/Report/"+run_time+".html", 'wb')
    runner = HTMLTestRunner(stream=fp,title='自动化测试报告',description='测试报告')
    suite = unittest.defaultTestLoader.discover('.', 'test*.py')
    runner.run(suite)