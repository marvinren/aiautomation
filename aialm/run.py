from aiautomation.testcase.test_case_generator import TestcaseGenerator
from aiautomation.utils.config import Config

body = b'{"caseId":102801,"env":166,"planId":627,"planBatchId":"627_20180122180933","execBatchId":"2018012218093328","caseExecId":1151424,"status":null,"failReason":null,"machine":"1000","parentExecId":null,"parentCaseId":null,"mode":null,"dataMapList":[],"origin":null,"uiScrpit":"# -*- coding: UTF-8 -*-\\n# \xe7\x99\xbb\xe5\xbd\x95\\r\\n# \xe6\x89\x93\xe5\xbc\x80\xe7\xbd\x91\xe5\x9d\x80\\r\\nopen_url(\'http://172.30.126.82:8080/webframe\')\\r\\nwait_for_load()\\r\\nloginUserName = \'admin\'\\r\\nloginPassword = \'123456\'\\r\\n# \xe8\xbe\x93\xe5\x85\xa5\xe8\xb4\xa6\xe5\x8f\xb7\xe5\x8f\x8a\xe5\xaf\x86\xe7\xa0\x81\\r\\nElement(loc=\'/html/body/div[2]/div[2]/form/div[1]/div/div/input\',l_type=\'XPATH\').input(loginUserName)\\r\\nElement(loc=\'/html/body/div[2]/div[2]/form/div[2]/div/div/input\',l_type=\'XPATH\').input(loginPassword)\\r\\n\\r\\n# \xe7\x82\xb9\xe5\x87\xbblogin\xe6\x8c\x89\xe9\x92\xae\\r\\nButton(loc=\'/html/body/div[2]/div[2]/form/div[4]/button\',l_type=\'XPATH\').click(delay=1)\\r\\nwait_for_load()\\r\\n\\r\\nerr_msg = \'\xe5\xb8\x90\xe5\x8f\xb7\xe5\xaf\x86\xe7\xa0\x81\xe4\xb8\x8d\xe6\xad\xa3\xe7\xa1\xae\'\\r\\n\\r\\n\\r\\nexpectValue = \'\xe8\xb4\xa6\xe6\x88\xb7\'\\r\\n#\xe5\xa6\x82\xe6\x9e\x9c\xe9\xa1\xb5\xe9\x9d\xa2\xe4\xb8\x8a\xe5\x87\xba\xe7\x8e\xb0\xe5\xb8\x90\xe6\x88\xb7\xe4\xb8\xa4\xe4\xb8\xaa\xe5\xad\x97\xef\xbc\x8c\xe5\x88\x99\xe8\xaf\x81\xe6\x98\x8e\xe6\x98\xaf\xe6\x88\x90\xe5\x8a\x9f\xe7\x9a\x84\\r\\nAssert.element_is_exist(loc=\'//*[@id=\\"container\\"]/div[1]/div/ul/li[4]/a/span[1]\',l_type=\'XPATH\',msg=err_msg)\\n\\n\\n","stressScrpit":null,"cpuUsed":null,"memeryUsed":null,"ip":null,"hostName":null,"createTime":null,"state":null,"onOffErr":null,"userName":null,"url":null,"agentId":null,"execType":"UI","propPool":null,"planDataId":null,"scriptName":null,"timeout":null,"planType":null,"threshold":null}'

t = TestcaseGenerator(Config("./config.yml").getConfig())
# t.get_test_module(2)
case_id = 2
case_exec_id = 62
try:
    t.connection()
    t.write_pages("./pages", case_id)
    t.write_case("./cases", case_id, case_exec_id)
finally:
    t.disconnection()

