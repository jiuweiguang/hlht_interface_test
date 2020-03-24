import pymysql
import time

#查询token值
def query_token_result(operator_id):
    db = pymysql.connect('127.0.0.1', 'root', 'hard1358', 'hlht_test')
    cursor = db.cursor()
    sql = "SELECT * FROM token_result WHERE opertor_id=" + "'" + operator_id +"'"+ " " + "limit 1"
    cursor.execute(sql)
    result = cursor.fetchall()
    if result:
        for i in result:
            data = {"operatorid":i[0],
                    "token_result":i[1]}
            return data
    else:
        db.close()
        return ""

#插入token值
def inster_token_result(operator_id,token_result):
    db = pymysql.connect('127.0.0.1', 'root', 'hard1358', 'hlht_test')
    cursor = db.cursor()
    data = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
    sql = "INSERT INTO `hlht_test`.`token_result`(`opertor_id`, `token_result`, `create_time`) VALUES (" + "'" +operator_id + "'"+ "," + "'"+token_result + "'" + ',' + "'" + data + "'"+ ')'
    try:
        cursor.execute(sql)
        db.commit()
        print("插入数据库成功")
    except:
        db.rollback()
        print("插入数据库失败")

#更新token值
def update_token_reslut(operator_id,token_result):
    db = pymysql.connect('127.0.0.1', 'root', 'hard1358', 'hlht_test')
    cursor = db.cursor()
    data = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    sql = "UPDATE `hlht_test`.`token_result` SET `token_result` = " + "'"+str(token_result)+"'" + ", `create_time` = " + "'" + str(data) + "'" + " WHERE `opertor_id` = " + "'"+operator_id+"'"
    try:
        cursor.execute(sql)
        db.commit()
        print("更新数据库成功")
    except:
        print("更新数据库失败")



def inster_start_result(post_data,bill_pay_no,resultCode,test_id,response_time):
    db = pymysql.connect('127.0.0.1', 'root', 'hard1358', 'hlht_test')
    cursor = db.cursor()
    data = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    if bill_pay_no == '':
        data_str = '{' + '"qrCode":' + '"' + str(post_data['qrCode']) + '"' + ',' + '"appFrom":' + '"' + str(post_data['appFrom']) + '"' + ',' +'"consId":' + '"' + str(post_data['consId']) + '"' + '}'
    else:
        data_str = '{' + '"qrCode":' + '"' + str(post_data['qrCode']) + '"' + ',' + '"appFrom":' + '"' + str(post_data['appFrom']) + '"' + ',' +'"consId":' + '"' + str(post_data['consId']) + '"' + ',' + \
                   '"billPayNo":' + '"' + bill_pay_no + '"' + '}'
    sql = "INSERT INTO `hlht_test`.`appstart`(`post_data`, `bill_pay_no` , `resultCode`,`test_id`,`time`,`response_time`) VALUES (" + "'" +data_str + "'"+ "," + "'"+bill_pay_no + "'" + ',' + "'" + resultCode + "'" + ','\
          + "'" + str(test_id) + "'" + ',' + "'" + data + "'" + ',' + "'" + str(response_time) + "'" + ')'
    try:
        cursor.execute(sql)
        db.commit()
        print("插入数据库成功")
    except Exception as e:
        db.rollback()
        print(e)
        print("插入数据库失败")

def inster_stop_result(bill_pay_no,resultCode,test_id,response_time):
    db = pymysql.connect('127.0.0.1', 'root', 'hard1358', 'hlht_test')
    cursor = db.cursor()
    data = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    sql = "INSERT INTO `hlht_test`.`appstop`(`bill_pay_no`, `resultCode` , `test_id`,`time`,`response_time`) VALUES (" + "'"+bill_pay_no + "'" + ',' + "'" + resultCode + "'" + ','\
          + "'" + str(test_id) + "'" + ',' + "'" + data + "'"+ ',' + "'" + str(response_time) + "'" + ')'
    try:
        cursor.execute(sql)
        db.commit()
        print("插入数据库成功")
    except:
        db.rollback()
        print("插入数据库失败")

def inster_querystate_result(data,bill_pay_no,resultCode,test_id,response_time):
    db = pymysql.connect('127.0.0.1', 'root', 'hard1358', 'hlht_test')
    cursor = db.cursor()
    time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    sql = "INSERT INTO `hlht_test`.`appquerystate`(`data`, `bill_pay_no` , `resultCode`,`test_id`,`time`,`response_time`) VALUES (" + "'" +data + "'"+ "," + "'"+bill_pay_no + "'" + ',' + "'" + resultCode + "'" + ','\
          + "'" + str(test_id) + "'" + ',' + "'" + time_now + "'" + ',' + "'" + str(response_time) + "'" +')'
    try:
        cursor.execute(sql)
        db.commit()
        print("插入数据库成功")
    except:
        db.rollback()
        print("插入数据库失败")

if __name__=='__main__':
    data=query_token_result('MA5F31P75')
    print(data)
    update_token_reslut('1','6666666')
    inster_token_result('5','65654565')