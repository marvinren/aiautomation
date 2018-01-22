from aiautomation.log.abstract_log import AbstractLog
from aiautomation.utils.log import get_logger

'''
写入控制台和文件的日志
'''


class SimpleLog(AbstractLog):

    def step_log_before(self, oper_type, oper_name, oper_id, parent_oper_id=None, *key, **kwargs):
        if oper_type == AbstractLog.STEP_TYPE_COMPONENT:
            self.log.info("S.[%s] %s 开始执行...." % (oper_type, oper_name))

    def step_log_after(self, oper_type, oper_name, oper_id, oper_time, result, log_content, parent_oper_id=None, *key,
                       **kwargs):
        if result == AbstractLog.SUCCESS_STATUS:
            self.log.info("E.[%s] %s 执行成功(用时%ss), %s" % (oper_type, oper_name, oper_time, log_content))
        else:
            self.log.error(
                "E.[%s.%s] 执行失败，结果为：%s, 执行时间为：%s具体日志为: %s" % (oper_type, oper_name, result, oper_time, log_content))

    def case_log_before(self, *key, **kwargs):
        self.log.info("S.[Case.%s.%s] 开始执行案例 ...." % (self.testcase.module_name, self.testcase.case_name))

    def case_log_after(self, result, run_time, log_content, *key, **kwargs):
        if result == AbstractLog.SUCCESS_STATUS:
            self.log.info("E.[Case.%s.%s] 执行成功, 执行时间为: %s" % (self.testcase.module_name, self.testcase.case_name, run_time))
        else:
            self.log.error("E.[Case.%s.%s] 执行成功执行失败(%s), 结果为：%s" % (self.testcase.module_name, self.testcase.case_name, result, log_content))

    def plan_log_before(self, *key, **kwargs):
        self.log.info("S.[Plan.%s.%s] 测试计划开始执行, 执行的批次号为[%s]..." % (self.testplan.plan_id, self.testplan.plan_name, self.testplan.exec_batch_id))

    def plan_log_after(self, *key, **kwargs):
        self.log.info("E.[Plan.%s.%s] 测试计划执行结束, 执行的批次号为[%s]" % (self.testplan.plan_id, self.testplan.plan_name, self.testplan.exec_batch_id))