# -*- coding: UTF-8 -*-

from ObjectAction import *
import os
import logging
import platform
import Assert
# from Timelimit
from threading import Thread


class TimeoutException(Exception):
    pass


ThreadStop = Thread._Thread__stop  # 获取私有函数


def timelimited(timeout):
    def decorator(function):

        def decorator2(*args, **kwargs):

            class TimeLimited(Thread):
                def __init__(self, _error=None, ):
                    Thread.__init__(self)
                    self._error = _error

                def run(self):
                    try:
                        self.result = function(*args, **kwargs)
                    except Exception, e:
                        self._error = e

                def _stop(self):
                    if self.isAlive():
                        ThreadStop(self)

            set_timeout_state(False)
            t = TimeLimited()
            t.start()
            t.join(timeout)

            if isinstance(t._error, TimeoutException):
                t._stop()
                set_timeout_state()
                raise TimeoutException('执行脚本超时！')

            if t.isAlive():
                t._stop()
                set_timeout_state()
                raise TimeoutException('执行脚本超时！')

            if t._error is None:
                return t.result

        return decorator2

    return decorator


def run(file_name=''):
    try:

        logging.info(platform.system())
        logging.info(os.path.sep)

        # 初始化数据库
        init_db()

        # 获取case信息
        t_path = os.path.split(file_name)
        logging.info(t_path)
        tmp = t_path[1].split('.')[0]
        case_id = int(tmp.split('_')[0])
        case_exec_id = int(tmp.split('_')[1])

        # 初始化case信息
        logging.info('case_id:' + str(case_id))
        set_case_id(case_id)
        logging.info('case_exec_id:' + str(case_exec_id))
        set_case_exec_id(case_exec_id)

        # 判断脚本是否存在
        logging.info('file_name:' + file_name)
        if not os.path.isfile(file_name):
            raise Exception('未找到指定脚本: %s' % file_name)
        else:
            try:
                # 初始化浏览器
                init_driver()

                # 执行脚本
                execfile(file_name)
                logging.info('脚本执行成功!')
                return None
            except WebDriverException, ex:
                error = 'WebDriver异常:%s' % ex
                logging.error(error)
                add_oper_log('ERROR', error)

                raise Exception(error)
            except BaseException, ex:
                error = '脚本执行异常:%s' % ex
                logging.error(error)
                add_oper_log('ERROR', error)

                raise Exception(error)
    except BaseException, ex:

        error = '脚本执行失败:%s' % ex
        logging.error(error)
        # raise BaseException(error)
        return error


def run_case(file_name='', timeout=None):
    @timelimited(timeout)
    def run_timeout(file_name):
        return run(file_name)

    return run_timeout(file_name)
