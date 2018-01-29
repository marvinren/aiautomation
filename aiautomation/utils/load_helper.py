import sys
import traceback
from imp import reload


def import_class(import_str):
    """
        加载module（带class）
    """
    mod_str, _sep, class_str = import_str.rpartition('.')
    __import__(mod_str)
    try:
        #reload(sys.modules[mod_str])
        return getattr(sys.modules[mod_str], class_str)
    except AttributeError:
        raise ImportError('Class %s cannot be found (%s)' %
                          (class_str,
                           traceback.format_exception(*sys.exc_info())))


def import_object(import_str, *args, **kwargs):
    """
    根据路径加载class，并创建对象
    :param import_str:
    :param args:
    :param kwargs:
    :return:
    """
    return import_class(import_str)(*args, **kwargs)


def import_module(import_str):
    """
    导入module
    """
    __import__(import_str)
    return sys.modules[import_str]