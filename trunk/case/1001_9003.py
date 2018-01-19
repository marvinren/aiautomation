#!/user/bin/env python
# -*- coding: UTF-8 -*-

from ObjectAction import *

open_url('http://10.251.22.103:37302//')
Element(loc='//div[contains(text(),"系统账户登录")]', l_type='XPATH').click()
Input(loc='input[name="username"]', l_type='CSS').input('admin')
Input(loc='input[name="password"]', l_type='CSS').input('admin_test')
Button(loc='button[type="submit"]', l_type='CSS').click(1)
# Link(loc='TestProduct-hph', l_type='PARTIAL').click(1)
# Link(loc='TestProduct-hph', l_type='PARTIAL').move_to(delay=5)
sleep(5)
# Element('搜索按钮').click()
# close_url()

# ObjectActionOld
# csInput('#kw', '', '亚信'.decode('utf-8'), 'stepname:查询信息,outputkey:NULL,group:1')
# time.sleep(1)
# csClick_v('#su')
# time.sleep(10)
# closeUrl()
