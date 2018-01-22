import traceback
from functools import wraps
import time

from aiautomation.log.abstract_log import AbstractLog
from aiautomation.testcase.test_case_module import CaseInfo


def step_log(step_type="Step", class_name=None, logger=None):
    def step_log_func(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            if logger is None:
                log = args[0].logger
            else:
                log = logger
            if class_name is not None:
                oper_name = "%s.%s" %(class_name, func.__name__)
            else:
                oper_name = func.__name__
            log.step_log_before(step_type, oper_name, None, None)
            start_time = time.time()
            ret = func(*args, **kwargs)
            end_time = time.time()
            log.step_log_after(step_type, oper_name, None, end_time - start_time, AbstractLog.SUCCESS_STATUS, "", None)
            return ret
        return wrap
    return step_log_func


def component(component_id=0):
    def component_func(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            component_name = func.__name__
            # 组件执行之前日志
            args[0].logger.step_log_before(AbstractLog.STEP_TYPE_COMPONENT, component_name, component_id)
            start_time = time.time()
            try:
                # 用例的具体执行
                func(*args, **kwargs)
                end_time = time.time()
                # 组件执行之后日志
                args[0].logger.step_log_after(AbstractLog.STEP_TYPE_COMPONENT, component_name, component_id,
                                              end_time - start_time, AbstractLog.SUCCESS_STATUS, "组件[%s]执行完毕" % component_name)
            except Exception as e:
                end_time = time.time()
                args[0].logger.step_log_after(AbstractLog.STEP_TYPE_COMPONENT, component_name, component_id,
                                              end_time - start_time, AbstractLog.ERROR_STATUS, str(e))
                # 组件异常需要重新抛出
                raise

        return wrap

    return component_func


def testcase(case_id, module_id, case_exec_id=None, parent_exec_id=None, module_name=None, case_name=None):
    def case_func(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            # 如果案例名称或者模块名称不存在，则使用方法名和类名，分别代替案例名称和模块名称
            if case_name is None:
                cn = func.__name__
            else:
                cn = case_name

            if module_name is None:
                mn = args[0].__class__.__name__
            else:
                mn = module_name
            case_info = CaseInfo(module_name = mn, case_name = cn, case_id = case_id, module_id = module_id, case_exec_id = case_exec_id, parent_exec_id = parent_exec_id)
            # 设置logger
            args[0].logger.get_logger("%s.%s" % (args[0].__class__.__name__, func.__name__))

            # 根据注解参数注入case_info
            args[0].case_info = case_info
            args[0].logger.case_log_before()
            start_time = time.time()
            try:
                # 先要执行场景恢复
                args[0].recovery()

                # 执行具体的测试用例
                func(*args, **kwargs)
                end_time = time.time()
                args[0].logger.case_log_after(AbstractLog.SUCCESS_STATUS, end_time - start_time,
                                              "案例[%s]执行成功" % case_info.case_name)
            except Exception as e:
                end_time = time.time()
                args[0].logger.case_log_after(AbstractLog.ERROR_STATUS, end_time - start_time, str(e))
                args[0].logger.error(traceback.format_exc())
                args[0].logger.error(e)

                # raise
            finally:
                # 执行完成执行回复操作，包括：清空case_info
                args[0].resume()

        return wrap

    return case_func


