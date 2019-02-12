import  unittest,time,os
from utils.HTMLTestRunner import HTMLTestRunner
from utils.config import Config, REPORT_PATH, CASE_PATH
from utils.mail import Email

description = Config().get('DESCRIPTION')
reporttitle = Config().get('REPORTTITLE')
title = Config().get('TITLE')
message =  Config().get('MESSAGE')
receiver = Config().get('RECEIVER')
server =  Config().get('SERVER')
sender =  Config().get('SENDER')
password = Config().get('PASSWORD')

def find_last_file(dir):
    file_lists = os.listdir(dir)
    file_lists.sort(key=lambda fn: os.path.getmtime(dir + "\\" + fn)
                    if not os.path.isdir(dir + "\\" + fn) else 0)
    newfile = os.path.join(dir,file_lists[-1])
    return  newfile

def create_report():
    # test_suit = unittest.TestSuite()
    discover = unittest.defaultTestLoader.discover(CASE_PATH, pattern='test_*.py', top_level_dir=None)
    # for test in discover:
    #     for test_case in test:
    #         test_suit.addTest(test_case)
    now=time.strftime('%Y-%m-%d_%H_%M',time.localtime(time.time()))
    report = REPORT_PATH + '\\report%s.html'%now
    last_file = find_last_file(REPORT_PATH)
    with open(report, 'wb') as f:
        runner = HTMLTestRunner(f, verbosity=2, title=reporttitle,description=description)
        runner.run(discover)

    e = Email(title=title, message=message,receiver=receiver,server=server,sender=sender,password=password,path=last_file)
    e.send()

