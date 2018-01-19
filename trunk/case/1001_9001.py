#!/user/bin/env python
# -*- coding: UTF-8 -*-

# from ObjectAction import *


# open_url('http://www.360doc.com/content/12/1006/21/9369336_239836993.shtml')
# verify_code()

# open_url('http://www.baidu.com')
# Element('搜索框').input('亚信')
# Element('搜索按钮').move_to(delay=5)
# Element('搜索按钮').click()
# close_url()

open_url('http://www.baidu.com')
# Input(loc='#kw', l_type='CSS').input('亚信')
Input(loc='#kw', l_type='CSS').input('selenium')
Input(loc='#su', l_type='CSS').click(delay=1)
sleep(5)
# close_url()


# ObjectActionOld
# csInput('#kw', '', '亚信'.decode('utf-8'), 'stepname:查询信息,outputkey:NULL,group:1')
# time.sleep(1)
# csClick_v('#su')
# time.sleep(10)
# closeUrl()
