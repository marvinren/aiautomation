# -*- coding: UTF-8 -*-

import time, datetime
from selenium import webdriver
from selenium.webdriver.support.expected_conditions import *
from selenium.webdriver.support.select import Select

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchFrameException as NoSuchFrameException, \
    NoAlertPresentException
from selenium.common.exceptions import NoSuchElementException as NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException as UnexpectedAlertPresentException
from selenium.common.exceptions import NoSuchWindowException as NoSuchWindowException
from selenium.common.exceptions import ElementNotVisibleException as ElementNotVisibleException
from selenium.common.exceptions import TimeoutException as TimeoutException
from OcrMod import getChr, getSplitLenth
# 这个包下的代码只允许打印debug日志，自定义的debug，因为selenium模块会打出很多debug日志
import random
import socket
import logging
import subprocess
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import *
from selenium.webdriver.common.by import By
import codecs
import Ocr

# 接口函数使用
import urllib2
import cookielib
import time
import json
import shutil
import linecache
from email.mime.text import MIMEText
import smtplib
from encodings import gbk
# from email.header import Header

# about send mail
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.encoders import encode_base64

# other.py user
import sqlite3
from ExecuteDb import *

from StepReport import StepReport
import platform
from selenium.webdriver.common.action_chains import *

import RunCase

# 数据库驱动
EX = None
# 浏览器驱动
WD = None
# ActionChains驱动
AC = None

Cnt = 0  # 用于自动截图
TmpCnt = 0  # 兼容ie6，7用，计数，暂时无用
curFrameLoc = [0, 0]  # 当前frame的坐标，用来计算绝对位置
# 记录时间差
sTime = None
eTime = None
# =========
cookie = None

# 用例数据
case_id = 0
case_exec_id = 0

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='./logs/log',
                    filemode='w')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler();
console.setLevel(logging.INFO);
# set a format which is simpler for console use
formatter = logging.Formatter('LINE %(lineno)-4d : %(levelname)-8s %(message)s');
# tell the handler to use this format
console.setFormatter(formatter);
logging.getLogger('').addHandler(console);

TIMEOUT_STATE = False


def set_timeout_state(state=True):
    global TIMEOUT_STATE
    TIMEOUT_STATE = state


# 日志装饰器---------------------------------------------------------
def log(inFunc):
    # global WD

    def wrapper(*args, **kw):

        # global WD
        # 内部函数不打印函数开始和结束信息
        rr = ""
        for i in args:
            if type(i) == str:
                rr = rr + ",\"" + i + "\""
            else:
                rr = rr + "," + str(i)
        rr = "function < " + inFunc.__name__ + "(" + rr[1:] + ") > start"
        # rr = rr.decode('utf-8').encode('gbk')
        rr = rr.decode('utf-8')
        logging.info(rr)
        # 获取参数需要区分执行模式
        tmp = inFunc(*args, **kw)
        rr = ""
        for i in args:
            if type(i) == str:
                rr = rr + ",\"" + i + "\""
            else:
                rr = rr + "," + str(i)
        rr = "function < " + inFunc.__name__ + "(" + rr[1:] + ") > end"
        # rr = rr.decode('utf-8').encode('gbk')
        rr = rr.decode('utf-8')
        logging.info(rr)
        return tmp

    return wrapper


# 日志装饰器---------------------------------------------------------------


# ----------------------    通用函数    ---------------------------
def set_case_exec_id(exec_id):
    global case_exec_id
    case_exec_id = exec_id


def get_case_exec_id():
    global case_exec_id
    return case_exec_id


def set_case_id(id):
    global case_id
    case_id = id


def get_case_id():
    global case_id
    return case_id


def init_db():
    """
    初始化DB
    :return:
    """
    global EX

    if EX is None:
        EX = ExecuteDb()


def init_driver():
    """
    初始化webdriver驱动和db
    :return:
    """
    global WD, AC

    if WD is None:
        driver = CONFIG['driver']
        if driver == 'Chrome':
            if platform.system() == 'Darwin':
                options = webdriver.ChromeOptions()
                options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
                WD = webdriver.Chrome(chrome_options=options)
            else:
                # 杀掉IE进程
                # os.system("taskkill -f /im Chrome.exe")
                # 杀掉IEDriverServer进程
                # os.system("taskkill -f /im chromedriver.exe")
                options = webdriver.ChromeOptions()
                options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
                WD = webdriver.Chrome(executable_path=CONFIG['driver_path'] + 'chromedriver.exe',
                                      chrome_options=options)
        elif driver == 'IE':
            # 杀掉IE进程
            os.system("taskkill -f /im iexplore.exe")
            # 杀掉IEDriverServer进程
            os.system("taskkill -f /im IEDriverServer.exe")

            WD = webdriver.Ie(executable_path=CONFIG['driver_path'] + 'IEDriverServer.exe')
        elif driver == 'Firefox':
            WD = webdriver.Firefox()
        elif driver == 'Edge':
            WD = webdriver.Edge(executable_path=CONFIG['driver_path'] + 'MicrosoftWebDriver.exe')
        elif driver == 'Safari':
            WD = webdriver.Safari()
        else:
            raise Exception('不支持的浏览器类型!')

        WD.set_page_load_timeout(30)

        # WD = webdriver.Ie(executable_path=CONFIG['path'] + '\\IEDriverServer.exe')
        # WD = webdriver.Chrome()

        AC = ActionChains(WD)


@log
def get_element(name):
    """
    获取元素信息
    :param name: 元素名称
    :return:
    """
    global EX
    return EX.get_element(name)


@log
def add_oper_log(oper_type, oper_name, value='', operator='', expect_value=''):
    """
    生成操作日志
    :param oper_type:
    :param oper_name:
    :param value:
    :param operator:
    :param expect_value:
    :return:
    """
    global EX, case_exec_id, case_id

    if TIMEOUT_STATE:
        raise Exception("脚本执行已超时！")

    node_log = {'oper_type': oper_type, 'oper_name': oper_name, 'value': value, 'operator': operator,
                'expect_value': expect_value, 'case_id': case_id, 'case_exec_id': case_exec_id,
                'node_id': 0, 'component_id': 0}
    EX.add_node_log(node_log)


@log
def case_exec_finsh(status=9, fail_reason=''):
    """
    用例执行完成后更新状态
    :param status: 状态(9:脚本执行成功 11:失败)
    :param fail_reason: 失败原因
    :return:
    """
    global EX, case_exec_id

    EX.update_case_exec_status(case_exec_id, status, fail_reason)


def get_veify_code():
    """
    获取验证码
    :return:
    """
    global WD

    try:
        x = CONFIG['verify_x']
        y = CONFIG['verify_y']
        w = CONFIG['verify_w']
        h = CONFIG['verify_h']

        img_path = '../img/region.png'
        WD.get_screenshot_as_file(img_path)

        file_1 = Ocr.cut_image(img_path, x, y, w, h)

        file_2 = Ocr.clear_noise(file_1)

        txt = Ocr.ocr_text(file_2)

        logging.info('veify_code = ' + txt)
    except Exception, ex:
        logging.error(ex)
        txt = ''

    return txt


# ----------------------    页面操作函数    ---------------------------
@log
def cs_find_element(loc, l_type):
    global WD

    switcher = {
        'ID': By.ID,
        'XPATH': By.XPATH,
        'LINK': By.LINK_TEXT,
        'PARTIAL': By.PARTIAL_LINK_TEXT,
        'NAME': By.NAME,
        'TAG': By.TAG_NAME,
        'CLASS': By.CLASS_NAME,
        'CSS': By.CSS_SELECTOR,
    }
    by = switcher.get(l_type, By.CSS_SELECTOR)

    j = 0
    while j < CONFIG['TimeOut']:
        try:
            e = WD.find_element(by, loc)
            if e.is_displayed() and e.is_enabled():
                return e
            else:
                raise ElementNotVisibleException(l_type + ' selector:"' + loc + '" not visible or not enabled')
        except Exception, ex:
            WD.switch_to_default_content()
            j = j + 1
            time.sleep(1)
            if type(ex) == NoSuchElementException or type(ex) == ElementNotVisibleException:
                # _autoSwitchFramesByJs(loc)
                pass
            if type(ex) == TimeoutException:
                logging.log(15, "page load timeout,try input again")
                return
    raise NoSuchElementException(
        '[%s]:[%s] wait over time for %ss \n' % (str(by), str(loc), str(CONFIG['TimeOut'])))


@log
def cs_find_elements(loc, l_type, key=''):
    global WD

    switcher = {
        'ID': By.ID,
        'XPATH': By.XPATH,
        'LINK': By.LINK_TEXT,
        'PARTIAL': By.PARTIAL_LINK_TEXT,
        'NAME': By.NAME,
        'TAG': By.TAG_NAME,
        'CLASS': By.CLASS_NAME,
        'CSS': By.CSS_SELECTOR,
    }
    by = switcher.get(l_type, lambda: By.CSS_SELECTOR)

    j = 0
    while j < CONFIG['TimeOut']:
        try:
            e = WD.find_elements(by, loc)
            if key == '':
                if len(e) > 0 and e[0].is_displayed() and e[0].is_enabled():
                    return e[0]
                raise ElementNotVisibleException(l_type + ' selector:"' + loc + '" not visible')
            else:
                if len(e) > 0:
                    for i in e:
                        if i.text.strip() == key and i.is_displayed() and i.is_enabled():
                            return i
                raise NoSuchElementException(l_type + ' selector:"' + loc + '" no such element')
        except Exception, ex:
            # print str(j)+"times"
            # print 'switch to default_content'
            WD.switch_to_default_content()
            time.sleep(1)
            j = j + 1
            if type(ex) == NoSuchElementException or type(ex) == ElementNotVisibleException:
                # _autoSwitchFramesByJs(loc, Keystr)
                pass
            if type(ex) == TimeoutException:
                logging.log(15, "page load timeout,try click again")
                return
    raise NoSuchElementException('wait over time for ' + str(CONFIG['TimeOut']) + 's' + ':\n')


@log
def cs_wait_for_load():
    global WD

    wait = WebDriverWait(WD, 30)
    wait.until(lambda x: WD.execute_script('return document.readyState') == 'complete', '页面加载超时!')


@log
def cs_clear(loc, l_type):
    cs_find_element(loc, l_type).clear()


@log
def cs_select_c(loc, l_type):
    global WD

    e = cs_find_element(loc, l_type)
    if not e.is_selected():
        e.click()


@log
def cs_deselect_c(loc, l_type):
    global WD

    e = cs_find_element(loc, l_type)
    if e.is_selected():
        e.click()


@log
def cs_clear(loc, l_type):
    global WD
    cs_find_element(loc, l_type).clear()


@log
def cs_is_selected(loc, l_type):
    global WD
    return cs_find_element(loc, l_type).is_selected()


@log
def cs_submit(loc, l_type):
    global WD
    return cs_find_element(loc, l_type).submit()


@log
def cs_exe_js(in_script):
    global WD

    try:
        r = WD.execute_script(in_script)
    except TimeoutException, e:
        logging.exception(e)
    return r


@log
def cs_open_url(url, timeout=-1):
    global WD, EX, case_exec_id
    if CONFIG["executeMode"] == 1:
        raise Exception('not suppurt!')
    else:
        j = 1
        while j < 5:
            try:
                if timeout > 0:
                    WD.set_page_load_timeout(timeout)
                    WD.set_script_timeout(timeout)
                WD.get(url)
                WD.delete_all_cookies()
                WD.refresh()
                WD.maximize_window()
                return
            except WebDriverException, ex:

                if str(ex.msg).__contains__('not reachable') or str(ex.msg).__contains__('no such window'):

                    logging.error('打开链接失败!原因: %s' % ex.msg)
                    logging.info('重新初始化浏览器!次数: %s' % j)
                    WD = None
                    init_driver()
                    j = j + 1
                else:
                    logging.warn('打开链接警告!原因: %s' % ex.msg)
                    return

        raise Exception("打开链接失败!")


@log
def cs_close_url():
    global WD, AC

    try:
        # time.sleep(1)
        WD.execute_script("window.opener=null;window.open('','_self');window.close();")
        time.sleep(1)
        WD.switch_to_alert().accept()
    except Exception, e:
        if type(e) == NoSuchWindowException or type(e) == NoAlertPresentException:
            pass
    WD.quit()
    WD = None
    AC = None


@log
def cs_close_window(*input_param):
    # 关闭当前窗口，要关闭指定窗口，用到后期再增加
    global WD
    if CONFIG["executeMode"] == 1:
        input_param = [] if len(input_param) == 0 else input_param[0]
    else:
        input_param = list(input_param)
    if len(input_param) == 0:
        try:
            WD.close()
        except:
            logging.info('no driver or driver with no window')
    else:

        i = 0
        while i < CONFIG['TimeOut']:
            tmp_str = input_param[0].decode('utf-8')
            for j in WD.window_handles:
                WD.switch_to_window(j)
                if WD.title == tmp_str:
                    WD.close()
                    return
            time.sleep(1)
            i = i + 1
        raise NoSuchWindowException('没有符合条件的窗口!')


@log
def switch_alert(chs=""):
    global WD
    if CONFIG["executeMode"] == 1:
        print 'not support!'
        raise SystemExit
    i = 0
    while i < CONFIG['TimeOut']:
        try:
            if chs == "":
                WD.switch_to_alert().accept()  # 点击弹出里面的确定按钮
            elif chs == "dismiss":
                WD.switch_to_alert().dismiss()  # 点击弹出上面的X按钮
            return
        except NoAlertPresentException:
            pass
        except UnexpectedAlertPresentException:
            pass
        except NoSuchWindowException:
            WD.switch_to_window(WD.window_handles[0])
        time.sleep(1)
        i = i + 1


# 尝试切换一个frame直到超时，30s
@log
def cs_switch_frame(loc, l_type):
    global WD
    if loc == '':
        logging.log(15, "准备切入default_content".decode('utf-8'))
        WD.switch_to_default_content()
    else:
        _waitElement(loc, l_type, True)
        logging.log(15, "准备切入frame by " + l_type + ":".decode('utf-8') + loc)
        WD.switch_to.frame(cs_find_element(loc, l_type))


@log
def cs_switch_window(title='', index=0):
    global WD

    # WD.switch_to_window(WD.window_handles[1])
    # return True
    n = 0
    for j in WD.window_handles:
        WD.switch_to_window(j)
        logging.info('window_handle[' + str(n) + ']:' + j + ':' + WD.title)
        n = n + 1

    i = 0
    while i < CONFIG['TimeOut']:
        try:
            if title == '' and index == 0:
                WD.switch_to_window(WD.window_handles[0])
                return True
            elif title != '':
                # print len(WD.window_handles)
                tmpStr = title.decode('utf-8')
                for j in WD.window_handles:
                    WD.switch_to_window(j)
                    # print WD.execute_script("return document.title")
                    # print tmpStr
                    # print WD.title
                    if WD.title == tmpStr:
                        return True
                return False
            else:
                WD.switch_to_window(WD.window_handles[index])
                return True
        except Exception, e:
            if e == UnexpectedAlertPresentException:
                logging.log(15, "Alert window exist,close and wait 1 seconds")
            if e == NoSuchWindowException:
                logging.log(15, "window not found,wait 1 seconds")
            i = i + 1
            time.sleep(1)
    return False


@log
def cs_select(loc, l_type, value='', index='', text=''):
    # 改造使用js操作选择select，selenium原生方法太慢
    global WD
    logging.log(15, "select value is able to be operated")

    if len(text) > 0:
        sel = cs_find_element(loc, l_type)
        Select(sel).select_by_visible_text(text)
        logging.log(15, "find text ok")
    elif len(index) > 0:
        sel = cs_find_element(loc, l_type)
        Select(sel).select_by_index(index)
        logging.log(15, "find index ok")
    else:
        sel = cs_find_element(loc, l_type)
        Select(sel).select_by_value(value)
        logging.log(15, "find value ok")


@log
def cs_deselect(loc, l_type, value='', index='', text=''):
    # 改造使用js操作选择select，selenium原生方法太慢
    global WD
    logging.log(15, "select value is able to be operated")

    if len(text) > 0:
        sel = cs_find_element(loc, l_type)
        Select(sel).deselect_by_visible_text(text)
        logging.log(15, "find text ok")
    elif len(index) > 0:
        sel = cs_find_element(loc, l_type)
        Select(sel).deselect_by_index(index)
        logging.log(15, "find index ok")
    else:
        sel = cs_find_element(loc, l_type)
        Select(sel).deselect_by_value(value)
        logging.log(15, "find value ok")


@log
def cs_deselect_all(loc, l_type):
    global WD
    logging.log(15, "select value is able to be operated")

    sel = cs_find_element(loc, l_type)
    Select(sel).deselect_all()


@log
def cs_first_selected_option(loc, l_type):
    global WD
    logging.log(15, "select value is able to be operated")

    sel = cs_find_element(loc, l_type)
    return Select(sel).first_selected_option


@log
def cs_all_selected_options(loc, l_type):
    global WD
    logging.log(15, "select value is able to be operated")

    sel = cs_find_element(loc, l_type)
    return Select(sel).all_selected_options


@log
def cs_is_multiple(loc, l_type):
    global WD
    logging.log(15, "select value is able to be operated")

    sel = cs_find_element(loc, l_type)
    return Select(sel).is_multiple()


@log
def cs_alert_text(o_val=[]):
    global WD
    if CONFIG["executeMode"] == 1:
        print 'not support!'
        raise SystemExit
    i = 0
    text = ''
    while i < CONFIG['TimeOut']:
        try:
            text = WD.switch_to_alert().text.encode('utf-8')
            o_val.append(text.strip())
            return text.strip()
        except NoAlertPresentException:
            pass
            # raise NoAlertPresentException('没有找到弹出框!')
        except UnexpectedAlertPresentException:
            pass
            # raise UnexpectedAlertPresentException('没有找到弹出框!')
        except NoSuchWindowException:
            # logging.error('NoSuchWindowException')
            WD.switch_to_window(WD.window_handles[0])

        time.sleep(1)
        i = i + 1

    if text == '':
        raise Exception('没有找到弹出框!')


@log
def cs_input_v(loc, l_type, in_txt):
    e = cs_find_element(loc, l_type)
    e.clear()
    e.send_keys(in_txt.decode('utf-8'))
    return True


@log
def cs_click_v(loc, l_type, key_str=''):
    e = cs_find_elements(loc, l_type, key_str)
    e.click()
    return True


@log
def cs_value_v(loc, l_type, attr):
    if attr == "html":
        tmp = cs_find_element(loc, l_type).text.encode('utf-8')
    else:
        tmp = cs_find_element(loc, l_type).get_attribute(attr).encode('utf-8')
    return tmp.strip()


@log
def cs_is_enabled(loc, l_type):
    try:
        e = cs_find_element(loc, l_type)
        if e.is_enabled() and e.is_displayed():
            logging.log(15, "element is ok to oper")
            return True
        else:
            return False
    except Exception, ex:
        logging.log(15, "element not exist")
        return False


@log
def cs_is_display(loc, l_type):
    try:
        e = cs_find_element(loc, l_type)
        if e.is_displayed():
            logging.log(15, "element is ok to oper")
            return True
        else:
            return False
    except Exception, ex:
        logging.log(15, "element not exist")
        return False


@log
def cs_wait(loc, l_type):
    we = cs_find_elements(loc, l_type)
    if we.is_enabled():
        return True
    return False


@log
def cs_focus(loc, l_type, key_str=''):
    e = cs_find_elements(loc, l_type, key_str)
    if key_str == '' and e.is_enabled():
        WD.execute_script("arguments[0].focus();", e)
    elif len(key_str) > 0:
        e.click()
    return True


# ----------------------    鼠标键盘操作函数    ---------------------------
@log
def ac_move_to_element(loc, l_type):
    global AC
    e = cs_find_element(loc, l_type)
    AC.move_to_element(e).perform()


@log
def ac_click(loc, l_type):
    global AC
    e = cs_find_element(loc, l_type)
    AC.click(e).perform()


@log
def ac_context_click(loc, l_type):
    global AC
    e = cs_find_element(loc, l_type)
    AC.context_click(e).perform()


@log
def ac_db_click(loc, l_type):
    global AC
    e = cs_find_element(loc, l_type)
    AC.double_click(e).perform()


@log
def ac_click_and_hold(loc, l_type):
    global AC
    e = cs_find_element(loc, l_type)
    AC.click_and_hold(e).perform()


@log
def ac_drag_and_drop(loc, l_type, t_loc, t_type):
    global AC
    source = cs_find_element(loc, l_type)
    target = cs_find_element(t_loc, t_type)
    AC.drag_and_drop(source, target).perform()


@log
def ac_drag_and_drop_by_offset(loc, l_type, x, y):
    global AC
    e = cs_find_element(loc, l_type)
    AC.drag_and_drop_by_offset(e, x, y).perform()


@log
def ac_key_down(value, loc='', l_type=''):
    global AC

    switcher = {
        'CONTROL': Keys.CONTROL,
        'ALT': Keys.ALT,
        'SHIFT': Keys.SHIFT,
    }
    key = switcher.get(value, lambda: Keys.CONTROL)

    if len(loc) > 0 and len(l_type) > 0:
        e = cs_find_element(loc, l_type)
        AC.key_down(key, e).perform()
    else:
        AC.key_down(key).perform()


@log
def ac_key_up(value, loc='', l_type=''):
    global AC

    switcher = {
        'CONTROL': Keys.CONTROL,
        'ALT': Keys.ALT,
        'SHIFT': Keys.SHIFT,
    }
    key = switcher.get(value, lambda: Keys.CONTROL)

    if len(loc) > 0 and len(l_type) > 0:
        e = cs_find_element(loc, l_type)
        AC.key_up(key, e).perform()
    else:
        AC.key_up(key).perform()


@log
def ac_key_input(value, content, loc='', l_type=''):
    global AC

    switcher = {
        'CONTROL': Keys.CONTROL,
        'ALT': Keys.ALT,
        'SHIFT': Keys.SHIFT,
    }
    key = switcher.get(value, lambda: Keys.CONTROL)

    if len(loc) > 0 and len(l_type) > 0:
        e = cs_find_element(loc, l_type)
        AC.key_down(key, e).send_keys(content).key_up(key, e).perform()
    else:
        AC.key_down(key).send_keys(content).key_up(key).perform()


@log
def ac_move_by_offset(x, y):
    global AC
    AC.move_by_offset(x, y).perform()


@log
def ac_move_to_element_with_offset(loc, l_type, x, y):
    global AC
    e = cs_find_element(loc, l_type)
    AC.move_to_element_with_offset(e, x, y).perform()


@log
def ac_release(loc='', l_type=''):
    global AC
    if len(loc) > 0 and len(l_type) > 0:
        e = cs_find_element(loc, l_type)
        AC.release(e).perform()
    else:
        AC.release().perform()


# ----------------------    原有函数    ---------------------------
@log
def get_pic(*input_param):
    global WD, Cnt
    if CONFIG["executeMode"] == 1:
        innerParam = [] if len(input_param) == 0 else input_param[0]
    else:
        innerParam = list(input_param)
    if len(innerParam) > 0:
        savPath = CONFIG['path'] + '\\pic\\' + innerParam[0] + '.png'
    else:
        pname = (3 - len(str(Cnt))) * '0' + str(Cnt)
        pname = (3 - len(str(CONFIG['CaseNumber']))) * '0' + str(CONFIG['CaseNumber']) + pname
        savPath = CONFIG['path'] + '\\pic\\' + pname + '.png'
    WD.save_screenshot(savPath)
    Cnt += 1


@log
def reset_url(*input_param):
    global WD
    if CONFIG["executeMode"] == 1:
        WD.get(input_param[0][0])
    else:
        WD.get(input_param[0])


@log
def refresh():
    global WD
    try:
        WD.refresh()
    except TimeoutException, e:
        logging.exception(e)


@log
def clickElement_v(*inputParam):
    global WD
    if CONFIG["executeMode"] == 1:
        innerParam = [] if len(inputParam) == 0 else inputParam[0]
    else:
        innerParam = list(inputParam)
    _waitElement(innerParam[0])
    try:
        if innerParam[0][0] == "/":
            logging.log(15, "element disabled status is " + str(
                WD.find_element_by_xpath(innerParam[0]).get_attribute("disabled")))
            WD.find_element_by_xpath(innerParam[0]).click()
        else:
            logging.log(15, "element disabled status is " + str(
                WD.find_element_by_css_selector(innerParam[0]).get_attribute("disabled")))
            WD.find_element_by_css_selector(innerParam[0]).click()
        return True
    except UnexpectedAlertPresentException:
        WD.switch_to_alert().accept()
        logging.log(15, '这里要重新考虑下元素事件里面会弹出小窗的情况')
    except TimeoutException:
        logging.log(15, "page load timeout,try click again")
        return True


# 这个基本不需要了
# 0-元素id或xpath,1-属性名称,2-期望值
@log
def checkValue(*inputParam):
    global WD
    if CONFIG["executeMode"] == 1:
        innerParam = [] if len(inputParam) == 0 else inputParam[0]
    else:
        innerParam = list(inputParam)
    _waitElement(innerParam[0])
    # 这里要支持id，xpath查找，并支持所有属性和innerHTML文本比对
    if innerParam[0][0] == "/":
        if innerParam[1] == "html":
            tmp = WD.find_element_by_xpath(innerParam[0]).text
            # print tmp
        else:
            tmp = WD.find_element_by_xpath(innerParam[0]).get_attribute(innerParam[1])
    else:
        if innerParam[1] == "html":
            tmp = WD.find_element_by_css_selector(innerParam[0]).text
        else:
            tmp = WD.find_element_by_css_selector(innerParam[0]).get_attribute(innerParam[1])
    if tmp != innerParam[2]:
        CONFIG["CaseStatus"] = "fail"


@log
def inputText_v(*inputParam):
    global WD
    if CONFIG["executeMode"] == 1:
        innerParam = [] if len(inputParam) == 0 else inputParam[0]
    else:
        innerParam = list(inputParam)
    _waitElement(innerParam[0])
    try:
        if len(innerParam) == 1:
            # 通过输入框手工获取值，这里以后要考虑下如果是textarea的情况，不能使用value输入
            WD.execute_script("document.getElementById('" + innerParam[0] + "').value=prompt('input a value')")
        else:
            print innerParam[1].decode('utf-8')
            if innerParam[0][0] == "/":
                WD.find_element_by_xpath(innerParam[0]).send_keys(innerParam[1].decode('utf-8'))
            else:
                WD.find_element_by_css_selector(innerParam[0]).send_keys(innerParam[1].decode('utf-8'))
        return True
    except NoSuchElementException, e:
        logging.exception(e)
        return False
    except TimeoutException:
        logging.log(15, "page load timeout,try input again")
        return True


# 等待一个元素加载完成，不建议使用
@log
def waitElement(*inputParam):
    global WD
    tmps = CONFIG['TimeOut']
    if CONFIG["executeMode"] == 1:
        innerParam = [] if len(inputParam) == 0 else inputParam[0]
    else:
        innerParam = list(inputParam)
    while tmps > 0:
        try:
            if innerParam[0][0] == "/":
                if WD.find_element_by_xpath(innerParam[0]):
                    return True
            else:
                if WD.find_element_by_css_selector(innerParam[0]):
                    return True
        except Exception, e:
            time.sleep(1)
            tmps = tmps - 1
    tmpstr = 'wait over time for ' + str(CONFIG['TimeOut']) + 's' + ': \n' + str(e)
    raise NoSuchElementException(tmpstr)


# 等待一个元素加载，内部调用，不考虑编码转换
def _waitElement(loc, l_type, tag=False):
    global WD
    tmps = CONFIG['TimeOut']
    while tmps > 0:
        try:
            e = cs_find_element(loc, l_type)
            if e.is_enabled() and (e.is_displayed() or tag == True):
                return
            else:
                time.sleep(1)
                tmps = tmps - 1
        except Exception, e:
            if type(e) != NoSuchElementException and type(e) != NoSuchFrameException:
                logging.exception(e)
                break
            time.sleep(1)
            tmps = tmps - 1
    tmpstr = 'wait over time for ' + str(CONFIG['TimeOut']) + 's' + ':\n'
    raise NoSuchElementException(tmpstr)


@log
def get_config(key_str):
    tmp = ''
    if key_str in CONFIG.keys():
        tmp = CONFIG[key_str]
    return tmp


@log
def getTitles(oVal=[]):
    global WD
    if CONFIG["executeMode"] == 1:
        print 'not support!'
        raise SystemExit
    try:
        tmpT = WD.title
        print tmpT
        tmpH = WD.current_window_handle
        if len(WD.window_handles) == 1:
            oVal.append(tmpT)
            return tmpT
        for j in WD.window_handles:
            WD.switch_to_window(j)
            oVal.append(WD.title.encode('utf-8'))
        WD.switch_to_window(tmpH)
    except Exception, e:
        logging.info('no driver or driver with no window')


@log
def getValue_v(Loc, Attr, InV=[]):
    global WD
    _waitElement(Loc)
    tmp = ''
    if Loc[0] == "/":
        if Attr == "html":
            tmp = WD.find_element_by_xpath(Loc).text
            if type(tmp) == unicode:
                tmp = tmp.encode('utf-8')
            InV.append(tmp)
        else:
            tmp = WD.find_element_by_xpath(Loc).get_attribute(Attr)
            if type(tmp) == unicode:
                tmp = tmp.encode('utf-8')
            InV.append(tmp)
    else:
        if Attr == "html":
            tmp = WD.find_element_by_css_selector(Loc).text
            if type(tmp) == unicode:
                tmp = tmp.encode('utf-8')
            InV.append(tmp)
        else:
            tmp = WD.find_element_by_css_selector(Loc).get_attribute(Attr)
            if type(tmp) == unicode:
                tmp = tmp.encode('utf-8')
            InV.append(tmp)
    return tmp.strip()


@log
def inputAuthCode(img='', input='', ex=0, ey=0, ew=0, eh=0):
    global WD
    innerParam = [img, input]
    _waitElement(innerParam[0])
    # 获取整个页面的截图
    savPath = CONFIG['path'] + '\\ocr'
    if os.path.isfile(savPath + '\\tmp_page.png'):
        os.system('del ' + savPath + '\\*.png')
    WD.save_screenshot(savPath + '\\tmp_page.png')
    # 通过传入的xywh坐标和宽长，使用nconvert抠出验证码图片并存为result.png
    if innerParam[0][0] == "/":
        e = WD.find_element_by_xpath(innerParam[0])
    else:
        e = WD.find_element_by_css_selector(innerParam[0])
    tmpCmd = savPath + "\\nconvert -quiet -o " + savPath + "\\result.png -crop "
    tmpCmd = tmpCmd + str(e.location.get('x') + ex) + ' ' + str(e.location.get('y') + ey) + ' ' + str(
        e.size.get('width') + ew) + ' ' + str(e.size.get('height') + eh)
    tmpCmd = tmpCmd + ' ' + savPath + "\\tmp_page.png"
    # print tmpCmd
    os.system(tmpCmd)

    # 返回的string写入web元素内
    authCode = getChr(savPath).strip()
    if innerParam[0][0] == "/":
        WD.find_element_by_xpath(innerParam[1]).clear()
        WD.find_element_by_xpath(innerParam[1]).send_keys(authCode)
    else:
        WD.find_element_by_css_selector(innerParam[1]).clear()
        WD.find_element_by_css_selector(innerParam[1]).send_keys(authCode)
    if getSplitLenth() > 0:
        logging.warn(
            "the split length of bitmap file is <" + str(getSplitLenth()) + ">,check OcrMod if not correct")
        logging.log(15, "the auth code is:" + authCode)


def retFunc(rList='noCall'):
    # print sys._getframe().f_code.co_name
    f1 = eval(rList)
    return f1


def endVideo():
    if CONFIG['capScreen'] == "y":
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect(("127.0.0.1", 1415))
            s.send("end")
            buf = []
            d = s.recv(1024)
            buf.append(d)
            if ''.join(buf).strip() == "stoped":
                logging.info("Screen captured success,check file at video\\temp.cap")
            else:
                logging.warn("录制屏幕进程有异常，请检查!")
                # print ''.join(buf)
        except Exception, e:
            # logging.error(e)
            logging.error("no capture run")
        finally:
            s.close()


def setOutput(inputParam):
    # logging.log(15,inputParam.decode('utf-8'))
    if type(inputParam) == gbk:
        inputParam = inputParam.decode('gbk')
    if type(inputParam) == unicode:
        inputParam = inputParam.encode('utf-8')
    inputParam = inputParam.replace('\n', '|')
    if CONFIG['output'] == "":
        CONFIG['output'] = inputParam
    else:
        CONFIG['output'] = CONFIG['output'] + "|" + inputParam


# 新函数-----------------------------------------------------------------------
# _autoSwitchFrames函数比Js版本的慢，作废不用
def _autoSwitchFrames(inPath):
    # inPath must be css path
    global WD, ar
    tmpLen = len(WD.find_elements_by_css_selector(inPath))
    if tmpLen >= 1:
        # true代表找到元素
        ar = True
        return
    tmpLen = len(WD.find_elements_by_css_selector('frame,iframe'))
    if tmpLen == 0:
        return
    tmpFrame = range(0, tmpLen)
    # print tmpFrame
    for i in tmpFrame:
        try:
            print WD.find_elements_by_tag_name("iframe")[i].get_attribute("id")
            WD.switch_to_frame(i)
        except:
            print 'aa'
        CONFIG['curFrames'].append(i)
        _autoSwitchFrames(inPath)
        if ar:
            return
        WD.switch_to_default_content()
        CONFIG['curFrames'].pop()
        for j in CONFIG['curFrames']:
            WD.switch_to_frame(j)
        ar = False


def _autoSwitchFramesByJs(inPath, keystr=''):
    global WD, TmpCnt
    # 为ie7以下浏览器添加tag
    #     if TmpCnt==0:
    #         #ie7以下添加xqsa属性
    #         tmpJs='''
    #
    #         '''
    #         tmpJs=tmpJs.replace('XXXX',inPath)
    #         WD.execute_script(tmpJs)
    tmpJs = '''
function getFrames() {
  var getFlag=false;
  var arr=[];
  var arrid=[];
  var curWindow=window;
  var bver=0;
  var ts="function addQueryForCss(){if(!document.querySelectorAll){"
  ts=ts+"document.querySelectorAll = function (selectors){var telements=[];var elements=[];"
  ts=ts+"telements=document.body.getElementsByTagName('*');for (var i=0;i<telements.length;i++)"
  ts=ts+"{if (telements[i].xqsa=='0'){telements[i].removeAttribute('xqsa');elements.push(telements[i]);}}return elements;}}}"
  findElements=function (csspath,wd,keystr) {
    if (wd.document.readyState!='complete'){
        return;
    }
    if (bver==6 && !wd.document.getElementById('seleniumaddquery')){
          var jss = wd.document.createElement('script');
          jss.setAttribute('id', 'seleniumaddquery');
          jss.setAttribute('type', 'text/javascript');
          wd.document.getElementsByTagName('head')[0].appendChild(jss);
          wd.document.getElementById('seleniumaddquery').text=ts;
          wd.addQueryForCss();
      }
    var ecnt=wd.document.querySelectorAll(csspath);
    if (ecnt.length>0) {
        if(keystr==undefined || keystr==''){
          getFlag=true;
          return;
      }else{
          for(var i=0;i<ecnt.length;i++){
              if (ecnt[i].innerText==keystr){
                  getFlag=true;
                  return;
              }
          }
      }
    }
    if (wd.frames.length>0) {
        var j="";
        for (var i=0;i<wd.frames.length;i++) {
          //find frames down
          arr.push(i);
          j=wd.document.getElementsByTagName('iframe')[i].getAttribute('id');
          if (j==null) { j=i; }
          arrid.push(j);
          //alert("j:"+j);
          findElements(csspath,wd.frames[i]);
          //alert('return from find'+j);
          if (getFlag) {
              return;
          } else { arr.pop(); arrid.pop();}
        }
    } else { return; }
  }
    if (curWindow.frames.length>0) {
        if (navigator.appVersion.indexOf('MSIE 6.0')>0 || navigator.appVersion.indexOf('MSIE 7.0')>0){
            bver=6;
        }
      findElements("XXXX",curWindow);
      return arr.join()+'|'+arrid.join();
    } else { return '||'; }
}
return getFrames();
'''
    tmpJs = tmpJs.replace('XXXX', inPath)
    tmpJs = tmpJs.replace('YYYY', keystr)
    #     if inPath=="#selectCustomer_btnText":
    #         WD.switch_to_default_content()
    #         WD.switch_to_frame("mainFrame")
    #         WD.switch_to_frame("tab_desktop_100036")
    #         WD.switch_to_frame("ID_72254")
    #         tmpS="var style=document.createElement('style');"
    #         tmpS=tmpS+"document._qsa = [];document._qsa.push('a');document.documentElement.firstChild.appendChild(style);"
    #         tmpS=tmpS+"style.styleSheet.cssText=\"#selectCustomer_btnText {x-qsa:expression(this.style.mzoom=='1'?0:function(e){e.style.mzoom='1';alert(e.id);alert(document._qsa.length);var aaaa=e;}(this))}\";"
    #         tmpS=tmpS+"scrollBy(0, 0);alert(document._qsa.length);alert(typeof(aaaa));"
    #         print tmpS
    #         WD.execute_script(tmpS)
    #         pass
    tmpStr = tmpJs.decode('utf-8')
    # print tmpStr
    arrseq = WD.execute_script(tmpStr)
    # print arrseq
    if arrseq[0] == "|":
        logging.log(15, "element not exists in any frames or hidden!")
        TmpCnt += 1
        return "|"
    TmpCnt = 0
    arr, arrid = arrseq.split("|")
    for i in arr.split(','):
        WD.switch_to_frame(int(i))
    logging.log(15, 'frames id sequence is [' + arrid + ']')
    return arr


@log
def getAuthCode(Loc='', ex=0, ey=0, ew=0, eh=0):
    global WD
    if CONFIG["executeMode"] == 1:
        print 'not support'
        return
    # 获取元素在iframe中的绝对位置
    WD.switch_to_default_content()
    frames = _autoSwitchFramesByJs(Loc)
    WD.switch_to_default_content()
    ifX = ex
    ifY = ey
    if len(frames) > 0 and frames != "|":
        tmpF = frames.split(",")
        for i in tmpF:
            e = WD.find_elements_by_css_selector('iframe')[int(i)]
            ifX = ifX + e.location.get('x')
            ifY = ifY + e.location.get('y')
            WD.switch_to_frame(int(i))
        print ifX, ifY

    # 获取整个页面的截图
    savPath = CONFIG['path'] + '\\ocr'
    if os.path.isfile(savPath + '\\tmp_page.png'):
        os.system('del ' + savPath + '\\*.png')
    WD.save_screenshot(savPath + '\\tmp_page.png')
    # 通过传入的xywh坐标和宽长，使用nconvert抠出验证码图片并存为result.png
    if Loc[0] == "/":
        e = WD.find_element_by_xpath(Loc)
    else:
        e = WD.find_element_by_css_selector(Loc)
    tmpCmd = savPath + "\\nconvert -quiet -o " + savPath + "\\result.png -crop "
    tmpCmd = tmpCmd + str(e.location.get('x') + ifX) + ' ' + str(e.location.get('y') + ifY) + ' ' + str(
        e.size.get('width') + ew) + ' ' + str(e.size.get('height') + eh)
    tmpCmd = tmpCmd + ' ' + savPath + "\\tmp_page.png"
    # print tmpCmd
    os.system(tmpCmd)

    # 返回的string写入web元素内
    authCode = getChr(savPath)
    if getSplitLenth() > 0:
        logging.warn(
            "the split length of bitmap file is <" + str(getSplitLenth()) + ">,check OcrMod if not correct")
        logging.log(15, "the auth code is:" + authCode)
    return authCode


# 接口函数---------------------------------------------------
@log
def sendPost(url, sdata, sheader={}):
    global cookie
    if cookie == None:
        cookie = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    req = urllib2.Request(url)
    # 默认的header
    req.add_header('User-Agent', 'ATtester')
    req.add_header('Accept', 'text/plain')
    # 自动以文件头不为空，则加入
    if sheader != {}:
        for i in sheader.keys():
            req.add_header(i, sheader[i])
    rep = opener.open(fullurl=req, data=sdata)
    return rep.read()


@log
def sendGet(url, sheader={}):
    global cookie
    if cookie == None:
        cookie = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    req = urllib2.Request(url)
    # 默认的header
    req.add_header('User-Agent', 'ATtester')
    req.add_header('Accept', 'text/plain')
    # 自动以文件头不为空，则加入
    if sheader != {}:
        for i in sheader.keys():
            req.add_header(i, sheader[i])
    rep = opener.open(req)
    tmp = rep.read()
    # print tmp
    return tmp


def sendMail(inputParam={}):
    content = inputParam['content']
    msg = MIMEMultipart()
    msg.attach(MIMEText(content, 'html', 'utf-8'))
    smtp_server = inputParam['smtp_server']
    from_addr = inputParam['from_addr'].decode('utf-8')
    password = inputParam['password']
    to_addr = inputParam['to_addr']
    cc_addr = ''
    if 'cc_addr' in inputParam.keys():
        cc_addr = inputParam['cc_addr']
    title = inputParam['title']
    if 'attach' in inputParam.keys():
        attachFile = inputParam['attach']
        # add attachment start
        attach = MIMEBase('application', 'octet-stream')
        attach.set_payload(file(CONFIG['path'] + 'temp\\' + attachFile, 'rb').read())
        encode_base64(attach)
        attach.add_header('Content-Disposition', 'attachment', filename=attachFile)
        msg.attach(attach)
        # add attachment end
    msg['From'] = from_addr
    msg['To'] = to_addr.decode('utf-8')
    if cc_addr != '':
        msg['Cc'] = cc_addr.decode('utf-8')
        to_addr = to_addr + "," + cc_addr
    # join Cc and To

    msg['Subject'] = Header(title.decode('utf-8'))
    try:
        server = smtplib.SMTP(smtp_server, 25)
        # server.set_debuglevel(1)
        server.login(from_addr, password)
        tmpMap = server.sendmail(from_addr, to_addr.split(','), msg.as_string())
        # print tmpMap
        print 'send ok,quit later'
        server.quit()
        if tmpMap == {}:
            r = 'ok'
        else:
            r = str(tmpMap)
        return r
    except Exception, e:
        # server.quit()
        logging.exception(e)
        return 'send mail error'


@log
def clearCookie():
    global cookie
    cookie = None


# new search frame
def csClick_p(Loc, Keystr=''):
    global WD
    frames = WD.FindElements(WD.By.TagName("frame"))
    for frame in frames:
        print frame

        # foreach (var frame in frames)
        # {
        #     if (frame.GetAttribute("name") == "ControlPanelFrame")
        #     {
        #         controlPanelFrame = frame;
        #         break;
        #     }
        # }
        #
        # if (controlPanelFrame != null)
        # {
        #     driver.SwitchTo().Frame(controlPanelFrame);
        # }
        #
        # // find the spane by id in frame "ControlPanelFrame"
        # Se.IWebElement spanElement = driver.FindElement(Se.By.Id("testcategory"));


def new_identity_id(province=45, city=01, district=03):
    """
    随机生成18位身份证号码
    :param province:省代码
    :param city:市代码
    :param district:区县代码
    :return:18位身份证号
    """
    arr = (7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2)  # 校验权重
    last = ('1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2')
    t = time.localtime()[0]
    # 450103 199001012062
    x = '%02d%02d%02d%04d%02d%02d%03d' % (province,
                                          city,
                                          district,
                                          random.randint(t - 25, t - 18),
                                          random.randint(1, 12),
                                          random.randint(1, 28),
                                          random.randint(1, 999))
    y = 0
    for i in range(17):
        y += int(x[i]) * arr[i]
    print '%s%s' % (x, last[y % 11])
    return '%s%s' % (x, last[y % 11])
