# -*- coding: UTF-8 -*-

from PackFunction import *


class Element(object):
    """
    元素类
    """

    def __init__(self, name='', loc='', l_type='', e_name='元素', e_type='元素'):
        """
        初始化元素
        :param name: 元素名
        :param loc: 定位值
        :param l_type: 定位类型
        :param e_name: 自定义元素名
        :param e_type: 自定义元素类型
        """
        if name != '':
            self.name = name
            e = get_element(name)

            if not e or len(e) == 0:
                raise Exception('没有找到元素！元素名:' + name)
            else:
                self.locator = e[0][0]
                self.locator_type = e[0][1]
                self.type = e_type
        else:
            self.locator = loc
            self.locator_type = l_type
            self.name = e_name
            self.type = e_type

    def input(self, content, delay=0):
        """
        WEB操作，文本框输入
        :param content: 输入内容
        :param delay: 延时
        :return:
        """
        time.sleep(delay)
        add_oper_log('STEP', '在[' + self.name + '][' + self.locator + ']中输入[' + content + ']')
        cs_input_v(self.locator, self.locator_type, content)

    def click(self, delay=0):
        """
        点击 按钮、link、其他需要点击的对象
        :param delay: 延时
        :return:
        """
        time.sleep(delay)
        add_oper_log('STEP', '单击[' + self.name + '][' + self.locator + ']')
        cs_click_v(self.locator, self.locator_type, '')

    def content_click(self, delay=0):
        """
        右键点击 按钮、link、其他需要点击的对象
        :param delay: 延时
        :return:
        """
        time.sleep(delay)
        add_oper_log('STEP', '右键点击[' + self.name + '][' + self.locator + ']')
        ac_context_click(self.locator, self.locator_type)

    def value(self, attr_name='html', delay=0):
        """
        获取属性值
        :param attr_name: 属性名
        :param delay: 延时
        :return:
        """
        time.sleep(delay)
        add_oper_log('STEP', '获取[' + self.name + '][' + self.locator + ']的属性值')
        attr_val = cs_value_v(self.locator, self.locator_type, attr_name)
        add_oper_log('STEP', '属性值为:' + attr_val)
        return attr_val

    def select(self, value='', index='', text='', delay=0):
        """
        选择下拉框的某一选项
        :param value: 选择的value属性
        :param index: 选择的index属性
        :param text: 选择的文本值
        :param delay: 延时
        :return:
        """
        time.sleep(delay)
        add_oper_log('STEP', '在下拉框:[' + self.name + '][' + self.locator + ']中选择[' + value + index + text + ']')
        cs_select(self.locator, self.locator_type, value, index, text)

    def deselect(self, value='', index='', text='', delay=0):
        """
        反选下拉框的某一选项
        :param value: 反选的value属性
        :param index: 反选的index属性
        :param text: 反选的文本值
        :param delay: 延时
        :return:
        """
        time.sleep(delay)
        add_oper_log('STEP', '在下拉框:[' + self.name + '][' + self.locator + ']中反选[' + value + index + text + ']')
        cs_deselect(self.locator, self.locator_type, value, index, text)

    def db_click(self, delay=0):
        """
        双击 按钮、link、其他需要点击的对象
        :param delay: 延时
        :return:
        """
        time.sleep(delay)
        add_oper_log('STEP', '双击[' + self.name + '][' + self.locator + ']')
        ac_db_click(self.locator, self.locator_type)

    def click_and_hold(self, delay=0):
        """
        点击鼠标左键，不松开
        :param delay: 延时
        :return:
        """
        time.sleep(delay)
        add_oper_log('STEP', '点击[' + self.name + '][' + self.locator + '],不松开')
        ac_click_and_hold(self.locator, self.locator_type)

    def drag_and_drop(self, target, delay=0):
        """
        将元素拖放至target元素处,然后松开鼠标
        :param self:
        :param target:
        :param delay:
        :return:
        """
        time.sleep(delay)
        add_oper_log('STEP',
                     '将将[' + self.name + '][' + self.locator + ']拖放至[' + target.name + '][' + target.locator + ']处')
        ac_drag_and_drop(self.locator, self.locator_type, target.locator, target.locator_type)

    def drag_and_drop_by_offset(self, x, y, delay=0):
        """
        拖拽到距离左上角(x,y)的坐标,然后松开鼠标
        :param self:
        :param x:
        :param y:
        :param delay: 延时
        :return:
        """
        time.sleep(delay)
        add_oper_log('STEP',
                     '将[' + self.name + '][' + self.locator + ']拖放至[' + str(x) + ',' + str(y) + ']处')
        ac_drag_and_drop_by_offset(self.locator, self.locator_type, x, y)

    def is_enabled(self, delay=0):
        """
        判断元素是否有效
        :param delay: 延时
        :return:
        """
        time.sleep(delay)
        add_oper_log('STEP', '判断[' + self.name + '][' + self.locator + ']是否有效')
        r = cs_is_enabled(self.locator, self.locator)
        add_oper_log('STEP', '[' + self.name + '][' + self.locator + ']有效状态为:' + str(r))

        return r

    def is_display(self, delay=0):
        """
        判断元素是否可见
        :param delay: 延时
        :return:
        """
        time.sleep(delay)
        add_oper_log('STEP', '判断[' + self.name + '][' + self.locator + ']是否可见')
        r = cs_is_display(self.locator, self.locator_type)
        add_oper_log('STEP', '[' + self.name + '][' + self.locator + ']可见状态为:' + str(r))

        return r

    def wait(self):
        """
        等待元素出现
        :return:
        """
        add_oper_log('STEP', '等待[' + self.name + '][' + self.locator + ']出现')
        r = cs_wait(self.locator, self.locator_type)
        add_oper_log('STEP', '[' + self.name + '][' + self.locator + ']出现状态为:' + str(r))

        return r

    def focus(self, delay=0):
        """
        聚焦元素
        :param delay: 延时
        :return:
        """
        time.sleep(delay)
        add_oper_log('STEP', '将焦点置于[' + self.name + '][' + self.locator + ']上')
        r = cs_focus(self.locator, self.locator_type)

        return r

    def deselect_all(self, delay=0):
        """
        反选下拉框的所有选项
        :param delay: 延时
        :return:
        """
        time.sleep(delay)
        add_oper_log('STEP', '反选下拉框[' + self.name + ']中所有选项')
        cs_deselect_all(self.locator, self.locator_type)

    def first_selected_option(self, delay=0):
        """
        返回下拉框的第一个选项
        :param delay: 延时
        :return:
        """
        time.sleep(delay)
        add_oper_log('STEP', '返回下拉框[' + self.name + ']中第一个选项')
        r = cs_first_selected_option(self.locator, self.locator_type)
        return r

    def all_selected_options(self, delay=0):
        """
        返回下拉框的第一个选项
        :param delay: 延时
        :return:
        """
        time.sleep(delay)
        add_oper_log('STEP', '返回下拉框[' + self.name + ']中所有选项')
        r = cs_all_selected_options(self.locator, self.locator_type)
        return r

    def is_multiple(self, delay=0):
        """
        判断是否为复选
        :param delay: 延时
        :return:
        """
        time.sleep(delay)
        add_oper_log('STEP', '开始判断下拉框[' + self.name + ']是否为复选')
        r = cs_is_multiple(self.locator, self.locator_type)
        add_oper_log('STEP', '下拉框[' + self.name + ']的复选判断为:' + str(r))
        return r

    def clear(self, delay=0):
        """
        清空元素值
        :param delay: 延时
        :return:
        """
        time.sleep(delay)
        add_oper_log('STEP', '清空[' + self.name + ']')
        cs_clear(self.locator, self.locator_type)

    def click_select(self, delay=0):
        """
        选择CheckBox/Radio
        :param delay: 延时
        :return:
        """
        time.sleep(delay)
        add_oper_log('STEP', '选择' + self.type + '[' + self.name + '][' + self.locator + ']')
        cs_select_c(self.locator, self.locator_type)

    def click_deselect(self, delay=0):
        """
        取消选择CheckBox/Radio
        :param delay: 延时
        :return:
        """
        time.sleep(delay)
        add_oper_log('STEP', '选择' + self.type + '[' + self.name + '][' + self.locator + ']')
        cs_deselect_c(self.locator, self.locator_type)

    def is_selected(self, delay=0):
        """
        判断CheckBox/Radio是否被选择
        :param delay: 延时
        :return:
        """
        time.sleep(delay)
        add_oper_log('STEP', '判断' + self.type + '[' + self.name + '][' + self.locator + ']是否被选择')
        r = cs_is_selected(self.locator, self.locator_type)
        add_oper_log('STEP', 'CheckBox[' + self.name + '][' + self.locator + ']选择状态为:' + str(r))

    def submit(self, delay=0):
        """
        表单提交
        :param delay: 延时
        :return:
        """
        time.sleep(delay)
        add_oper_log('STEP', '表单[' + self.name + '][' + self.locator + ']提交')
        cs_submit(self.locator, self.locator_type)

    def key_down(self, key, delay=0):
        """
        在元素上按下某个修改键(CONTROL,ALT,SHIFT)
        :param key: CONTROL,ALT,SHIFT
        :param delay:
        :return:
        """
        time.sleep(delay)
        add_oper_log('STEP', '按下[' + self.name + '][' + self.locator + ']上的键[' + key + ']')
        ac_key_down(key, self.locator, self.locator_type)

    def key_up(self, key, delay=0):
        """
        在元素上松开某个修改键(CONTROL,ALT,SHIFT)
        :param key: CONTROL,ALT,SHIFT
        :param delay:
        :return:
        """
        time.sleep(delay)
        add_oper_log('STEP', '松开[' + self.name + '][' + self.locator + ']上的键[' + key + ']')
        ac_key_up(key, self.locator, self.locator_type)

    def key_input(self, key, content, delay=0):
        """
        在元素上输入复合键，如：ctrl+c
        :param key: CONTROL,ALT,SHIFT
        :param content: 输入内容
        :param delay:
        :return:
        """
        time.sleep(delay)
        add_oper_log('STEP', '在[' + self.name + '][' + self.locator + ']上按下复合键[' + key + ']＋[' + content + ']')
        ac_key_input(key, content, self.locator, self.locator_type)

    def release(self, delay=0):
        """
        在元素上松开鼠标
        :param self:
        :param delay:
        :return:
        """
        time.sleep(delay)
        add_oper_log('STEP', '放开[' + self.name + '][' + self.locator + ']上的鼠标')
        ac_release(self.locator, self.locator_type)

    def move_to(self, delay=0):
        """
        鼠标移动到元素上
        :param self:
        :param delay:
        :return:
        """
        time.sleep(delay)
        add_oper_log('STEP', '将鼠标移动到[' + self.name + '][' + self.locator + ']上')
        ac_move_to_element(self.locator, self.locator_type)

    def move_to_element_with_offset(self, x, y, delay=0):
        """
        鼠标移动距离左上角(x,y)的位置
        :param self:
        :param x:
        :param y:
        :param delay:
        :return:
        """
        time.sleep(delay)
        add_oper_log('STEP', '将鼠标移动到距离[' + self.name + '][' + self.locator + ']左上角[' + str(x) + '，' + str(y) + ']的位置')
        ac_move_to_element_with_offset(self.locator, self.locator_type, x, y)


class Form(Element):
    """
    Form类
    """

    def __init__(self, name='', loc='', l_type='', e_name='元素'):
        """
        初始化Radio
        :param name: Radio名
        """
        super(Form, self).__init__(name, loc, l_type, e_name, 'Form')


class Link(Element):
    """
    Link类
    """

    def __init__(self, name='', loc='', l_type='', e_name='元素'):
        """
        初始化Radio
        :param name: Radio名
        """
        super(Link, self).__init__(name, loc, l_type, e_name, '链接')


class Button(Element):
    """
    Button类
    """

    def __init__(self, name='', loc='', l_type='', e_name='元素'):
        """
        初始化Radio
        :param name: Radio名
        """
        super(Button, self).__init__(name, loc, l_type, e_name, '按钮')


class Input(Element):
    """
    Input类
    """

    def __init__(self, name='', loc='', l_type='', e_name='元素'):
        """
        初始化Radio
        :param name: Radio名
        """
        super(Input, self).__init__(name, loc, l_type, e_name, '文本框')


class Select(Element):
    """
    Select类
    """

    def __init__(self, name='', loc='', l_type='', e_name='元素'):
        """
        初始化Radio
        :param name: Radio名
        """
        super(Select, self).__init__(name, loc, l_type, e_name, '下拉框')


class Radio(Element):
    """
    Radio类
    """

    def __init__(self, name='', loc='', l_type='', e_name='元素'):
        """
        初始化Radio
        :param name: Radio名
        """
        super(Radio, self).__init__(name, loc, l_type, e_name, 'Radio')


class CheckBox(Element):
    """
    CheckBox类
    """

    def __init__(self, name='', loc='', l_type='', e_name='元素'):
        """
        初始化CheckBox
        :param name: CheckBox名
        """
        super(CheckBox, self).__init__(name, loc, l_type, e_name, 'CheckBox')


# -----------------------     鼠标键盘操作方法    -----------------------
def key_down(key, delay=0):
    """
    按下某个修改键(CONTROL,ALT,SHIFT)
    :param key: CONTROL,ALT,SHIFT
    :param delay:
    :return:
    """
    time.sleep(delay)
    add_oper_log('STEP', '按下键[' + key + ']')
    ac_key_down(key)


def key_up(key, delay=0):
    """
    松开某个修改键(CONTROL,ALT,SHIFT)
    :param key: CONTROL,ALT,SHIFT
    :param delay:
    :return:
    """
    time.sleep(delay)
    add_oper_log('STEP', '松开键[' + key + ']')
    ac_key_up(key)


def key_input(key, content, delay=0):
    """
    在元素上输入复合键，如：ctrl+c
    :param key: CONTROL,ALT,SHIFT
    :param content: 输入内容
    :param delay:
    :return:
    """
    time.sleep(delay)
    add_oper_log('STEP', '按下复合键[' + key + ']＋[' + content + ']')
    ac_key_input(key, content)


def move_by_offset(x, y, delay=0):
    """
    移动到距离当前位置(x,y)的点
    :param x:
    :param y:
    :param delay:
    :return:
    """
    time.sleep(delay)
    add_oper_log('STEP', '将鼠标移动到坐标[' + str(x) + '，' + str(y) + ']')
    ac_move_by_offset(x, y)


def release(delay=0):
    """
    松开鼠标
    :param delay:
    :return:
    """
    time.sleep(delay)
    add_oper_log('STEP', '放开鼠标')
    ac_release()


# -----------------------     页面通用操作方法    -----------------------
def sleep(second=0):
    """
    进程睡眠
    :param second: 睡眠时长(秒)
    :return:
    """
    add_oper_log('STEP', '进程睡眠[' + str(second) + ']秒')
    time.sleep(second)


def open_url(url):
    """
    打开链接
    :param url: 链接地址
    :return:
    """
    add_oper_log('STEP', '打开链接[' + url + ']')
    cs_open_url(url)


def close_url(delay=0):
    """
    关闭链接
    :return:
    """
    time.sleep(delay)
    cs_close_url()
    add_oper_log('STEP', '关闭浏览器')


def exe_js(script, delay=0):
    """
    执行JS脚本
    :param script: 脚本内容
    :param delay: 延时
    :return:
    """
    time.sleep(delay)
    add_oper_log('STEP', '开始执行脚本:' + script)
    r = cs_exe_js(script)
    add_oper_log('STEP', '脚本执行结果:[' + r + ']')
    return r


def wait_for_load():
    """
    等待页面加载
    :return:
    """
    add_oper_log('STEP', '等待页面加载')
    cs_wait_for_load()
    add_oper_log('STEP', '页面加载完成')


def close_window(title, delay=0):
    """
    关闭窗口
    :param title:
    :param delay:
    :return:
    """
    time.sleep(delay)
    add_oper_log('STEP', '关闭窗口:[' + title + ']')
    cs_close_window(title)


def switch_to_alert(chs='', delay=0):
    """
    切换到弹出框并点击
    :param chs: 点击确定为空，点击取消为dismiss
    :param delay: 延时
    :return:
    """
    time.sleep(delay)
    alert = cs_alert_text()
    add_oper_log('STEP', '切换到弹出框:[' + alert + ']并点击:[' + ('' == chs and '确定' or '取消') + ']')
    switch_alert(chs)


def switch_to_frame(loc='', l_type='', delay=0):
    """
    切换到frame
    :param loc: 定位值，为空则切换到默认frame
    :param l_type: 定位类型(id,name,xpath,css等)
    :param delay: 延时
    :return:
    """
    time.sleep(delay)
    add_oper_log('STEP', '切换到frame:[' + loc + ']')
    cs_switch_frame(loc, l_type)


def switch_to_window(title='', index=0, delay=0):
    """
    切换到window
    :param title: 窗体名称，为空则切换到第一个窗体
    :param index: 窗体索引
    :param delay: 延时
    :return:
    """
    time.sleep(delay)
    add_oper_log('STEP', '切换到window:[' + title + ']')
    cs_switch_window(title, index)


# def show_alert():
#     alert = cs_alert_text()
#     add_oper_log('STEP', '弹出提示框:[' + alert + ']')


def alert_text(delay=0):
    """
    获取弹出框的值
    :param delay: 延时
    :return:
    """
    time.sleep(delay)
    add_oper_log('STEP', '开始获取弹出框内容')
    r = cs_alert_text(oVal=[])
    add_oper_log('STEP', '弹出框内容:' + r)
    return r


def verify_code(delay=0):
    """
    获取验证码
    :param delay: 延时
    :return:
    """
    time.sleep(delay)
    add_oper_log('STEP', '开始获取验证码')
    r = get_veify_code()
    add_oper_log('STEP', '验证码:' + r)
