# -*- coding: UTF-8 -*-

from ObjectAction import *


def element_is_exist(name='', loc='', l_type='', e_name='元素', msg='校验失败', delay=0):
    """
    判断元素是否存在
    :param name:
    :param loc:
    :param l_type:
    :param e_name:
    :param msg:
    :param delay:
    :return:
    """
    time.sleep(delay)

    add_oper_log('ASSERT', '开始判断元素是否存在')
    e = Element(name=name, loc=loc, l_type=l_type, e_name=e_name)
    try:
        e.wait()
    except:
        raise Exception('%s:没有找到符合条件的元素!' % msg)


def value_is_expect(name='', loc='', l_type='', e_name='元素', attr='html', expect='', msg='校验失败', delay=0):
    """
    判断元素值是否符合预期
    :param name:
    :param loc:
    :param l_type:
    :param e_name:
    :param attr:
    :param expect:
    :param msg:
    :param delay:
    :return:
    """
    add_oper_log('ASSERT', '开始判断元素值是否符合预期值:' + expect)
    e = Element(name=name, loc=loc, l_type=l_type, e_name=e_name)
    if not e.value(attr_name=attr, delay=delay) == expect:
        raise Exception('%s:元素值不符合预期!' % msg)
