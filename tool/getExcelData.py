import xlrd
import xlwt
from xlutils.copy import copy
import os

class getExcelData():
    data = []
    filepath = 'E:\\PycharmProjects\\hlht_interface_test\\tool\\hlht_case_test.xlsx'
    # filepath = 'E:\\PycharmProjects\\hlht_interface_test\\tool\\charge_test.xlsx'
    # filepath = 'E:\\PycharmProjects\\hlht_interface_test\\tool\\charge_test_one.xlsx'
    # filepath = 'E:\\PycharmProjects\\hlht_interface_test\\tool\\charge_test_stop.xlsx'
    # filepath = 'E:\\PycharmProjects\\hlht_interface_test\\tool\\charge_test_app_query_state.xlsx'

    def getData(self):
        try:
            self.file = xlrd.open_workbook(self.filepath)
            self.sheet_d =self.file.sheets()[0]
            self.nrows = self.sheet_d.nrows
            for i in range(1,self.nrows):
                self.data_dist = {"test_id": "",  # 用例ID
                             "test_name": "",  # 用例名称
                             "test_url": "",  # url
                             "test_addr": "",  # 接口地址
                             "test_data": "",  # 请求数据
                             "test_opertorid": "",  # 运营商标识
                             "test_operatorsecret": "",  # 运营商秘钥
                             "test_datasecret": "",  # 消息秘钥
                             "test_datasecretiv": "",  # 初始化向量
                             "test_sigsecret": "",# 签名秘钥
                             "test_ency":"" }# 是否加密
                self.data_dist['test_id'] = self.sheet_d.cell(i,0).value
                self.data_dist['test_name'] = self.sheet_d.cell(i,1).value
                self.data_dist['test_url'] = self.sheet_d.cell(i,2).value
                self.data_dist['test_addr'] = self.sheet_d.cell(i,3).value
                self.data_dist['test_data'] = str(self.sheet_d.cell(i,4).value)
                self.data_dist['test_opertorid'] = str(self.sheet_d.cell(i, 5).value)
                self.data_dist['test_operatorsecret'] = self.sheet_d.cell(i, 6).value
                self.data_dist['test_datasecret'] = self.sheet_d.cell(i, 7).value
                self.data_dist['test_datasecretiv'] = self.sheet_d.cell(i, 8).value
                self.data_dist['test_sigsecret'] = self.sheet_d.cell(i, 9).value
                self.data_dist['test_ency'] = self.sheet_d.cell(i,12).value
                self.data.append(self.data_dist)
            return self.data
        except Exception as e:
            print(e)
            return e

    def write_excel_xls_append(self,value):
        self.old_file = xlrd.open_workbook(self.filepath)
        self.new_excel  = copy(self.old_file)
        self.ws = self.new_excel.get_sheet(0)
        self.ws.write(1,13,value)
        self.new_excel.save('charge_test1.xls')



if __name__ =='__main__':
    data= getExcelData().write_excel_xls_append("test")
    # print(data)

