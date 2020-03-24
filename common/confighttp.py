import json
import requests
import simplejson

def post(header, address,data,timeout=30):
    """
    post 请求
    :param header:  请求头
    :param address:  host地址
    :param timeout: 超时时间
    :param data: 请求参数
    :param files: 文件路径
    :return:
    """
    data = json.dumps(data)
    response = requests.post(url=address, data=data, headers=header, timeout=timeout)
    try:
        return response.status_code, response.json(),response.elapsed.total_seconds()
    except json.decoder.JSONDecodeError:
        return response.status_code, ''
    except simplejson.errors.JSONDecodeError:
        return response.status_code, ''
    except Exception as e:
        raise

if __name__ == '__main__':
    data = {
  "OperatorID":"MA1GUT604",
  "Data":"y4MAW3YF9ZltQsdZoQwpXA2XOZ6Ga6+pjLqgbjsYi28MuOLA6eZw8dfZE3VoKag1gk2a1texuIkPZ/a1Gn8DwZib3Y7O+CA8bj1G4afkRnqI4TdWJipOxDVqX8CBQH4oWPv4LwdkaHdp/ZQm3Ay+8U4Se/WudA+9y+us3yVBoTUDGSnFpnsANhRN9mlgBzvcDNsO6lLwZRdCyocmJhuF+A==",
  "TimeStamp":"20191122091742",
  "Seq":"0001",
  "Sig":"EE9E2FB45B7F058FB2BA1326CE1BAD6D"
            }
    data_json = json.dumps(data)
    header = {"Content-Type":"application/json","Authorization":"Bearer 1154708ACF5EB0304E8B15733853A2E8"}
    response = requests.post(url="http://unions.carenergynet.cn/evcs/v20160701/query_stations_info", data=data_json, headers=header)
    print(response.text)
# def get(header, address, data, timeout=8):
#     """
#     get 请求
#     :param header:  请求头
#     :param address:  host地址
#     :param data: 请求参数
#     :param timeout: 超时时间
#     :return:
#     """
#     response = requests.get(url=address, params=data, headers=header, timeout=timeout)
#     if response.status_code == 301:
#         response = requests.get(url=response.headers["location"])
#     try:
#         return response.status_code, response.json()
#     except json.decoder.JSONDecodeError:
#         return response.status_code, ''
#     except simplejson.errors.JSONDecodeError:
#         return response.status_code, ''
#     except Exception as e:
#         logging.exception('ERROR')
#         logging.error(e)
#         raise
#
#
# def put(header, address, request_parameter_type, data=None, timeout=8, files=None):
#     """
#     put 请求
#     :param header:  请求头
#     :param address:  host地址
#     :param request_parameter_type: 接口请求参数格式 （form-data, raw, Restful）
#     :param data: 请求参数
#     :param timeout: 超时时间
#     :param files: 文件路径
#     :return:
#     """
#     if request_parameter_type == 'raw':
#         data = json.dumps(data)
#     response = requests.put(url=address, data=data, headers=header, timeout=timeout, files=files)
#     try:
#         return response.status_code, response.json()
#     except json.decoder.JSONDecodeError:
#         return response.status_code, ''
#     except simplejson.errors.JSONDecodeError:
#         return response.status_code, ''
#     except Exception as e:
#         logging.exception('ERROR')
#         logging.error(e)
#         raise
#
#
# def delete(header, address, data, timeout=8):
#     """
#     put 请求
#     :param header:  请求头
#     :param address:  host地址
#     :param timeout: 超时时间
#     :param data: 请求参数
#     :return:
#     """
#     response = requests.delete(url=address, params=data, headers=header, timeout=timeout)
#     try:
#         return response.status_code, response.json()
#     except json.decoder.JSONDecodeError:
#         return response.status_code, ''
#     except simplejson.errors.JSONDecodeError:
#         return response.status_code, ''
#     except Exception as e:
#         logging.exception('ERROR')
#         logging.error(e)
#         raise

