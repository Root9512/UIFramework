import  unittest,time,os
from utils.HTMLTestRunner import HTMLTestRunner
from utils.config import Config, REPORT_PATH, CASE_PATH

description = Config().get('DESCRIPTION')
reporttitle = Config().get('REPORTTITLE')
def create_report():
    # test_suit = unittest.TestSuite()
    discover = unittest.defaultTestLoader.discover(CASE_PATH, pattern='test_*.py', top_level_dir=None)
    # for test in discover:
    #     for test_case in test:
    #         test_suit.addTest(test_case)
    now=time.strftime('%Y-%m-%d_%H_%M',time.localtime(time.time()))
    report = REPORT_PATH + '\\report%s.html'%now
    with open(report, 'wb') as f:
        runner = HTMLTestRunner(f, verbosity=2, title=reporttitle,description=description)
        runner.run(discover)

