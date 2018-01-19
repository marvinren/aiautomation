#!/user/bin/env python
# -*- coding: UTF-8 -*-

from ObjectAction import *
import Assert

open_url('http://123.125.98.202:47048/essframe')

Input(name='CB_登陆_登录名').input(content='HUNP00', delay=0)
Input(name='CB_登陆_密码').input('cbss%1234')
Select(name='CB_登陆_省份').select(text='湖南', index='', value='', delay=0)
Button(name='CB_登陆_确定').click(delay=10)
wait_for_load()

switch_to_frame('navframe', 'ID')
Link(loc='FIRST_MENU_LINK_BIL6000', l_type='ID').click()

switch_to_frame()
switch_to_frame('sidebarframe', 'ID')
Link(loc='普通交费', l_type='LINK').click()
wait_for_load()

switch_to_frame()
switch_to_frame('contentframe', 'ID')
switch_to_frame('navframe_1', 'ID')
Input(loc='input[id="cond_SERIAL_NUMBER"]', l_type='CSS').input('18608480592')
Button(loc='input[id="bquerytopwithfee"]', l_type='CSS').click()
Input(loc='input[name="cond_TRADE_FEE"]', l_type='CSS').input('1')
Button(loc='input[id="bsubmit"]', l_type='CSS').click()

switch_to_window(title='交费确认', delay=0)
switch_to_frame('contentframe', 'ID')
Button(loc='input[id="bupdate"][type="button"]', l_type='CSS').click()
switch_to_alert(delay=0)
close_window('交费功能')


# close_url()

# ObjectActionOld
# csInput('#kw', '', '亚信'.decode('utf-8'), 'stepname:查询信息,outputkey:NULL,group:1')
# time.sleep(1)
# csClick_v('#su')
# time.sleep(10)
# closeUrl()
