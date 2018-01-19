import traceback
from functools import wraps
import time
from aiautomation.log.abstract_log import AbstractLog
from aiautomation.testcase.test_case import CaseInfo


def component(component_id=0):
    def component_func(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            case_info = args[0].case_info
            component_name = func.__name__
            if case_info is None:
                case_info = CaseInfo("", args[0].__class__.__name__, "", "", "")
            # 组件执行之前日志
            args[0].logger.before_step_log(AbstractLog.STEP_TYPE_COMPONENT, component_name, case_info.case_id,
                                           case_info.case_exec_id, case_info.node_id, component_id)
            start_time = time.time()
            try:
                # 用例的具体执行
                func(*args, **kwargs)
                end_time = time.time()
                # 组件执行之后日志
                args[0].logger.after_step_log(AbstractLog.STEP_TYPE_COMPONENT, component_name, case_info.case_id,
                                              case_info.case_exec_id, case_info.node_id, component_id,
                                              end_time - start_time, 0, "组件[%s]执行完毕" % component_name)
            except Exception as e:
                end_time = time.time()
                args[0].logger.after_step_log(AbstractLog.STEP_TYPE_COMPONENT, component_name, case_info.case_id,
                                              case_info.case_exec_id, case_info.node_id, component_id,
                                              end_time - start_time, 1, str(e))
                # 组件异常需要重新抛出
                raise

        return wrap

    return component_func


def testcase(case_id, case_exec_id, node_id, module_name=None, case_name=None):
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
            case_info = CaseInfo(mn, cn, case_id, case_exec_id, node_id)
            # 设置logger
            args[0].logger.get_logger("%s.%s" %(args[0].__class__.__name__, func.__name__))

            # 根据注解参数注入case_info
            args[0].case_info = case_info
            args[0].logger.before_case_log(case_info.case_id, case_info.case_exec_id, case_info.node_id,
                                           case_info.case_name, case_info.module_name)
            start_time = time.time()
            try:
                # 先要执行场景恢复
                args[0].recovery()

                # 执行具体的测试用例
                func(*args, **kwargs)
                end_time = time.time()
                args[0].logger.after_case_log(case_info.case_id, case_info.case_exec_id, case_info.node_id,
                                              case_info.case_name, case_info.module_name, 0, end_time - start_time,
                                              "案例[%s]执行成功" % case_info.case_name)
            except Exception as e:
                end_time = time.time()
                args[0].logger.after_case_log(case_info.case_id, case_info.case_exec_id, case_info.node_id,
                                              case_info.case_name, case_info.module_name, 1, end_time - start_time,
                                              str(e))
                args[0].logger.error(traceback.format_exc())
                args[0].logger.error(e)

                #raise
            finally:
                # 执行完成执行回复操作，包括：清空case_info
                args[0].resume()

        return wrap

    return case_func
