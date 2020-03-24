import json
import time
from common.confighttp import post
from tool.AES import AES_Decrypt,AES_Encrypt
from tool.connect_mysql import *
from tool.md5 import encryptHex2Upper
failureException = AssertionError


def post_interface(excl_data):
    all_data = {"test_id":excl_data["id"],
                "address":excl_data["address"],
                "data":excl_data["postdata"],
                "addr":excl_data["test_addr"],
                "datasecret":excl_data["datasecret"],
                "datasecretiv":excl_data["datasecretiv"],
                "operatorsecret":excl_data["operatorsecret"],
                "opertorid":str(excl_data["opertorid"]),
                "url":excl_data["url"],
                "sigsecret":excl_data["sigsecret"]
                }
    if excl_data["test_addr"] == '/query_token':
        heards = {"Content-Type": "application/json"}
        # query_token(heards=heards,address=address,data=data,datasecret=datasecret,datasecretiv=datasecretiv,opertorid=opertorid)
        query_token(heards=heards,data=all_data)
    elif excl_data["test_addr"] == '/query_stations_info':
        heards_charge = get_heards(data=all_data)
        query_stations_info(heards=heards_charge,data=all_data)
    elif excl_data["test_addr"] == '/query_station_status':
        heards_charge = get_heards(data=all_data)
        query_station_status(heards=heards_charge,data=all_data)
    elif excl_data["test_addr"] == '/query_equip_auth':
        heards_charge = get_heards(data=all_data)
        query_equip_auth(heards=heards_charge, data=all_data)
    elif excl_data["test_addr"] == '/query_equip_business_policy':
        heards_charge = get_heards(data=all_data)
        query_equip_business_policy(heards=heards_charge, data=all_data)
    elif excl_data["test_addr"] == '/query_start_charge':
        heards_charge = get_heards(data=all_data)
        query_start_charge(heards=heards_charge,data=all_data)
    elif excl_data["test_addr"] == '/query_equip_charge_status':
        heards_charge = get_heards(data=all_data)
        query_equip_charge_status(heards=heards_charge, data=all_data)
    elif excl_data["test_addr"] == '/query_stop_charge':
        heards_charge = get_heards(data=all_data)
        query_stop_charge(heards=heards_charge, data=all_data)
    elif excl_data["test_addr"] == '/check_charge_orders':
        pass
    elif excl_data["test_addr"] =='/appStartCharge':
        heards = {"Content-Type": "application/json"}
        result,response_time= appStartCharge(heards=heards,data=all_data)
        # result_str = json.loads(result['post_data'])
        inster_start_result(result['post_data'],result['bill_pay_no'],result['resultCode'],result['id'],response_time=response_time)

    elif excl_data["test_addr"] == '/appStopCharge':
        heards = {"Content-Type": "application/json"}
        appStopCharge(heards=heards, data=all_data)

    elif excl_data["test_addr"] == '/appQueryState':
        heards = {"Content-Type": "application/json"}
        appQueryState(heards=heards, data=all_data)

def query_token(heards,data):
    try:
        status_code, result,response_time = post(header=heards, address=data["address"],data=data["data"])
        result_data = result['Data']
        result_data_decrypt = AES_Decrypt(key=data["datasecret"], vi=data["datasecretiv"], data=result_data)
        result_data_decrypt_json = json.loads(result_data_decrypt)
        AccessToken = result_data_decrypt_json['AccessToken']
        print('status_code:%s\n' % status_code + 'token result:%s\n' % result + '解密数据%s\n' % result_data_decrypt_json)
        mysql_data = query_token_result(data["opertorid"])
        if mysql_data == '':
            inster_token_result(operator_id=data["opertorid"],token_result=AccessToken)
        elif mysql_data['token_result'] == AccessToken:
            pass
        elif mysql_data['token_result'] != AccessToken:
            update_token_reslut(data["opertorid"],AccessToken)
    except Exception as e:
        print(e)
        raise failureException("token失败")

def token_fail_re_token(url,data):
    try:
        heards = {"Content-Type": "application/json"}
        address_token = url + '/query_token'
        data_token = {"OperatorID": data["opertorid"], "OperatorSecret": data["operatorsecret"]}
        data_json = json.dumps(data_token)
        data_encrypt = AES_Encrypt(data=data_json, key=data["datasecret"], vi=data["datasecretiv"])
        time_now = time.strftime("%Y%m%d%H%M", time.localtime(time.time()))
        post_data = {"OperatorID": data["opertorid"],
                     "Data": data_encrypt,
                     "TimeStamp": time_now,
                     "Seq": "0001",
                     "Sig": encryptHex2Upper(key=data["sigsecret"], data=data["opertorid"] + data_encrypt + time_now + '0001')}
        token_data = {"address":address_token,
                      "data":post_data,
                      "datasecret":data["datasecret"],
                      "datasecretiv":data["datasecretiv"],
                      "opertorid":data["opertorid"]}
        query_token(heards=heards, data=token_data)
    except Exception as e:
        print(e)
        raise failureException("token失败")

def query_start_charge(heards,data):
    try:
        status_code, result,response_time = post(header=heards, address=data["address"], data=data["data"])
        if result['Ret']==4002:
            token_fail_re_token(url=data["url"], data=data)
            token_result = query_token_result(data["opertorid"])['token_result']
            if token_result == "":
                token_fail_re_token(url=data["url"], data=data)
            bear = "Bearer " + token_result
            heards_charge = {"Content-Type": "application/json", "Authorization": bear}
            query_start_charge(heards=heards_charge,data=data)
            # raise failureException("Token错误")
        elif result['Ret']==0:
            result_data = result['Data']
            result_data_decrypt = AES_Decrypt(key=data["datasecret"], vi=data["datasecretiv"], data=result_data)
            result_data_decrypt_json = json.loads(result_data_decrypt)
            print('status_code:%s\n'%status_code + 'token result:%s\n'%result + '解密数据%s\n'%result_data_decrypt_json)
    except Exception as e:
        print('启动失败')
        raise failureException("启动失败")

def query_stations_info(heards,data):
    try:
        status_code, result,response_time = post(header=heards, address=data["address"], data=data["data"])
        if result['Ret'] == 4002:
            token_fail_re_token(url=data["url"], data=data)
            token_result = query_token_result(data["opertorid"])['token_result']
            if token_result == "":
                token_fail_re_token(url=data["url"], data=data)
            bear = "Bearer " + token_result
            heards_charge = {"Content-Type": "application/json", "Authorization": bear}
            query_stations_info(heards=heards_charge, data=data)
        elif result['Ret'] == 0:
            result_data = result['Data']
            result_data_decrypt = AES_Decrypt(key=data["datasecret"], vi=data["datasecretiv"], data=result_data)
            result_data_decrypt_json = json.loads(result_data_decrypt)
            print('status_code:%s\n' % status_code + 'token result:%s\n' % result + '解密数据%s\n' % result_data_decrypt_json)
    except Exception as e:
        print('获取场站信息失败')
        raise failureException("获取场站信息失败")


def query_station_status(heards,data):
    try:
        status_code, result,response_time = post(header=heards, address=data["address"], data=data["data"])
        if result['Ret']==4002:
            token_fail_re_token(url=data["url"], data=data)
            token_result = query_token_result(data["opertorid"])['token_result']
            if token_result == "":
                token_fail_re_token(url=data["url"], data=data)
            bear = "Bearer " + token_result
            heards_charge = {"Content-Type": "application/json", "Authorization": bear}
            query_stop_charge(heards=heards_charge,data=data)
        elif result['Ret']==0:
            result_data = result['Data']
            result_data_decrypt = AES_Decrypt(key=data["datasecret"], vi=data["datasecretiv"], data=result_data)
            result_data_decrypt_json = json.loads(result_data_decrypt)
            print('status_code:%s\n'%status_code + 'token result:%s\n'%result + '解密数据%s\n'%result_data_decrypt_json)
    except Exception as e:
        print('获取场站信息失败')
        raise failureException("获取场站信息失败")

def query_stop_charge(heards,data):
    try:
        status_code, result,response_time = post(header=heards, address=data["address"], data=data["data"])
        if result['Ret']==4002:
            token_fail_re_token(url=data["url"], data=data)
            token_result = query_token_result(data["opertorid"])['token_result']
            if token_result == "":
                token_fail_re_token(url=data["url"], data=data)
            bear = "Bearer " + token_result
            heards_charge = {"Content-Type": "application/json", "Authorization": bear}
            query_stop_charge(heards=heards_charge,data=data)
        elif result['Ret']==0:
            result_data = result['Data']
            result_data_decrypt = AES_Decrypt(key=data["datasecret"], vi=data["datasecretiv"], data=result_data)
            result_data_decrypt_json = json.loads(result_data_decrypt)
            print('status_code:%s\n'%status_code + 'token result:%s\n'%result + '解密数据%s\n'%result_data_decrypt_json)
    except Exception as e:
        print('停止失败')
        raise failureException("停止失败")

def query_equip_auth(heards,data):
    try:
        status_code, result,response_time = post(header=heards, address=data["address"], data=data["data"])
        if result['Ret']==4002:
            token_fail_re_token(url=data["url"], data=data)
            token_result = query_token_result(data["opertorid"])['token_result']
            if token_result == "":
                token_fail_re_token(url=data["url"], data=data)
            bear = "Bearer " + token_result
            heards_charge = {"Content-Type": "application/json", "Authorization": bear}
            query_stop_charge(heards=heards_charge,data=data)
        elif result['Ret']==0:
            result_data = result['Data']
            result_data_decrypt = AES_Decrypt(key=data["datasecret"], vi=data["datasecretiv"], data=result_data)
            result_data_decrypt_json = json.loads(result_data_decrypt)
            print('status_code:%s\n'%status_code + 'token result:%s\n'%result + '解密数据%s\n'%result_data_decrypt_json)
    except Exception as e:
        print('设备认证失败')
        raise failureException("设备认证失败")

def query_equip_business_policy(heards,data):
    try:
        status_code, result,response_time = post(header=heards, address=data["address"], data=data["data"])
        if result['Ret']==4002:
            token_fail_re_token(url=data["url"], data=data)
            token_result = query_token_result(data["opertorid"])['token_result']
            if token_result == "":
                token_fail_re_token(url=data["url"], data=data)
            bear = "Bearer " + token_result
            heards_charge = {"Content-Type": "application/json", "Authorization": bear}
            query_stop_charge(heards=heards_charge,data=data)
        elif result['Ret']==0:
            result_data = result['Data']
            result_data_decrypt = AES_Decrypt(key=data["datasecret"], vi=data["datasecretiv"], data=result_data)
            result_data_decrypt_json = json.loads(result_data_decrypt)
            print('status_code:%s\n'%status_code + 'token result:%s\n'%result + '解密数据%s\n'%result_data_decrypt_json)
    except Exception as e:
        print('充电桩业务策略逻辑失败')
        raise failureException("充电桩业务策略逻辑失败")

def query_equip_charge_status(heards,data):
    try:
        # time.sleep(60)
        status_code, result,response_time = post(header=heards, address=data["address"], data=data["data"])
        if result['Ret']==4002:
            token_fail_re_token(url=data["url"], data=data)
            token_result = query_token_result(data["opertorid"])['token_result']
            if token_result == "":
                token_fail_re_token(url=data["url"], data=data)
            bear = "Bearer " + token_result
            heards_charge = {"Content-Type": "application/json", "Authorization": bear}
            query_stop_charge(heards=heards_charge,data=data)
        elif result['Ret']==0:
            result_data = result['Data']
            result_data_decrypt = AES_Decrypt(key=data["datasecret"], vi=data["datasecretiv"], data=result_data)
            result_data_decrypt_json = json.loads(result_data_decrypt)
            print('status_code:%s\n'%status_code + 'token result:%s\n'%result + '解密数据%s\n'%result_data_decrypt_json)
    except Exception as e:
        print('查询订单对应充电信息数据失败')
        raise failureException("查询订单对应充电信息数据失败")

def get_heards(data):
    try:
        token_result = query_token_result(data["opertorid"])['token_result']
        if token_result == "":
            token_fail_re_token(url=data["url"], data=data)
            token_result = query_token_result(data["opertorid"])['token_result']
        bear = "Bearer " + token_result
        heards_charge = {"Content-Type": "application/json", "Authorization": bear}
        return heards_charge
    except Exception as e:
        heards_charge = {"Content-Type": "application/json","Authorization": ""}
        return heards_charge

def appStartCharge(heards,data):
    try:
        write_data = {"id":data["test_id"],
                      "post_data":data['data'],
                      "bill_pay_no":"",
                      "resultCode":""}
        status_code, result,response_time = post(header=heards, address=data["address"], data=data["data"])
        print(status_code,result)
        if 'resultCode' in result:
            if result["resultCode"] == '00000':
                billPayNo = result["data"]["billPayNo"]
                write_data["bill_pay_no"] = billPayNo
                write_data['resultCode'] = result['resultCode']
                return write_data,response_time
            else:
                write_data["bill_pay_no"] = ''
                write_data['resultCode'] = result['resultCode']
                return write_data,response_time
        else:
            return write_data,response_time
    except Exception as e:
        return e

def appQueryState(heards,data):
    try:
        while True:
            status_code, result,response_time = post(header=heards, address=data["address"], data=data["data"])
            if result["resultCode"] == "00000":
                inster_querystate_result(data=json.dumps(result["data"]), bill_pay_no=data["data"]["billPayNo"],resultCode=result["resultCode"], test_id=data["test_id"],response_time=response_time)
            time.sleep(3)
            if result["resultCode"] != "00000":
                inster_querystate_result(data=json.dumps(result["data"]),bill_pay_no=data["data"]["billPayNo"],resultCode=result["resultCode"],test_id=data["test_id"],response_time=response_time)
                break
    except Exception as e:
        print(e)


def appStopCharge(heards,data):
    try:
        status_code, result,response_time = post(header=heards, address=data["address"], data=data["data"])
        inster_stop_result(bill_pay_no=data["data"]["billPayNo"],resultCode=result["resultCode"],test_id=data["test_id"],response_time=response_time)
        print(status_code,result)
    except Exception as e:
        print(e)

# if __name__ == '__main__':