from aiautomation.log.abstract_log import AbstractLog
from aiautomation.utils.log import get_logger

'''
写入控制台和文件的日志
'''


class SimpleLog(AbstractLog):

    def before_step_log(self, oper_type, oper_name, case_id, case_exec_id, node_id,
                        component_id, *key, **kwargs):
        self.log.info("S.%s[%s]...." % (oper_type, oper_name))

    def after_step_log(self, oper_type, oper_name, case_id, case_exec_id, node_id,
                       component_id, oper_time, result, log_content, *key, **kwargs):
        if result == 0:
            self.log.info("E.%s[%s]执行成功(用时%ss), %s" % (oper_type, oper_name, oper_time, log_content))
        else:
            self.log.error(
                "E.%s[%s]执行失败，结果为：%s, 执行时间为：%s具体日志为: %s" % (oper_type, oper_name, result, oper_time, log_content))

    def before_case_log(self, case_id, case_exec_id, node_id, case_name, module_name, *key, **kwargs):
        self.log.info("S.Case[%s:%s]开始执行案例 ...." % (module_name, case_name))

    def after_case_log(self, case_id, case_exec_id, node_id, case_name, module_name, result, run_time, log_content,
                       *key, **kwargs):
        if result == 0:
            self.log.info("E.Case[%s:%s]执行成功, 执行时间为: %s" % (module_name, case_name, run_time))
        else:
            self.log.error("E.Case[%s:%s]执行成功执行失败(%s), 结果为：%s" % (module_name, case_name, result, log_content))

    def element_log(self, case_id, case_exec_id, node_id, element, action):
        self.log.info("SE.ELEMENT 对控件[%s]进行操作[%s]" % (element, action))


