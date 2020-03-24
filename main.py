import time
from common.HTMLTestRunner_PY3 import HTMLTestRunner
import unittest
import os





if __name__ == '__main__':
    run_time = time.strftime('%Y-%m-%d_%H_%M_%S', time.localtime(time.time()))
    suite = unittest.defaultTestLoader.discover('.', 'test*.py')
    fp = open(os.getcwd()+"/Report/"+run_time+".html", 'wb')
    runner = HTMLTestRunner(stream=fp,
                            title='自动化测试报告',
                            description='测试报告')
    runner.run(suite)
    fp.close()
