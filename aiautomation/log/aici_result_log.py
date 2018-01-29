import datetime
import random

import pymysql

from aiautomation.log.abstract_log import AbstractLog
from aiautomation.log.simple_log import SimpleLog


class AiciResultLog(SimpleLog):
    """
        向数据库写入结果，但是使用的是单connection，可以考虑做一个数据库连接池
    """

    def __init__(self, config=None):
        SimpleLog.__init__(self, config)
        if config is None:
            raise AttributeError("AiciResultLog请注入config对象")
        self._host = config.aiautomation.agent.db_host
        self._port = config.aiautomation.agent.db_port
        self._user = config.aiautomation.agent.db_user
        self._pwd = config.aiautomation.agent.db_pwd
        self._dbname = config.aiautomation.agent.db_dbname

        self._conn = pymysql.connect(host=self._host, port=self._port, user=self._user, passwd=self._pwd,
                                     db=self._dbname, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    def disconnect(self):
        if self._conn is not None:
            self._conn.close()

    def safe(self, parameter):
        return pymysql.escape_string(str(parameter))

    def add_case_oper_log(self, **kwargs):
        if kwargs['component_id'] is None:
            kwargs['component_id'] = 0

        oper_type = "STEP"
        if AbstractLog.SUCCESS_STATUS != kwargs['result']:
            oper_type = "ERROR"
        sql = "insert into case_oper_log (oper_type, oper_name, value, operator, expect_value, oper_time, case_id, case_exec_id, node_id, component_id) " \
              "values ('%s','%s','%s','%s','%s',now(), %s, %s, %s, %s )" \
              % (oper_type, self.safe("%s:%s") % (kwargs['oper_name'], kwargs['log_content']), self.safe(kwargs['value']),
                 self.safe(kwargs['operator']), self.safe(kwargs['expect_value']), self.safe(kwargs['case_id']),
                 self.safe(kwargs['case_exec_id']), '0', self.safe(kwargs['component_id']))
        with self._conn.cursor() as cursor:
            self.log.debug("查询案例执行步骤说明: %s" % sql)
            cursor.execute(sql)
            self._conn.commit()

    def start_case_exec_log(self, **kwargs):
        with self._conn.cursor() as cursor:

            sql = "select case_id as 'id' from case_def where case_id = %d" % self.testcase.case_id
            cursor.execute(sql)
            result = cursor.fetchone()
            if result is None:
                sql = "INSERT INTO case_def VALUES ('%s', '%s', '', 'UI', 'SINGLE', '0', null, null, null, null, '1', '%s', '%s', '0')" \
                      % (self.testcase.case_id, self.testcase.case_name, self.testplan.product_id, self.testcase.module_id)
                cursor.execute(sql)
                self._conn.commit()
            else:
                sql = "update case_def set case_name='%s' where case_id = %d" % (self.testcase.case_name, self.testcase.case_id)
                cursor.execute(sql)
                self._conn.commit()

            count = 0
            if kwargs['case_exec_id'] is not None:
                cursor.execute("select count(*) as 'count' from case_exec_log where case_exec_id = '%s'" % kwargs['case_exec_id'])
                count = cursor.fetchone()['count']

            # 根据是否存在case_exec_log，进行插入或者更新数据
            if count == 0:
                sql = "INSERT INTO case_exec_log VALUES (null, '0', '%s', 'SINGLE', '0', '%s', '%s', '%s', " \
                      "'%s', null, null, null, '%s', null, " \
                      "now(), null, '%s', '%s', '%s', null)" \
                      % (self.safe(kwargs['case_id']),
                         self.safe(self.testplan.plan_id), self.safe(self.testplan.plan_batch_id),
                         self.safe(kwargs['exec_batch_id']),
                         AbstractLog.START_STATUS, "", self.safe(kwargs['machine_id']),
                         self.safe(kwargs['env_id']), self.safe(kwargs['product_id']))
                self.log.debug("生成新的case执行记录: %s" % sql)
                cursor.execute(sql)
                self._conn.commit()

                sql = "SELECT LAST_INSERT_ID() as 'id'"
                cursor.execute(sql)
                case_exec_id = cursor.fetchone()['id']
                self.debug("获取新的Case_exec_id为：%s" % case_exec_id)
                self.testcase.case_exec_id = case_exec_id
            else:
                self.log.warn("已经存在case_exec_id=%s的案例执行日志，进行更新" % kwargs['case_exec_id'])
                sql = "UPDATE case_exec_log set case_id = '%s'" \
                      ",status='%s', start_time=now(), end_time=NULL, fail_reason='' where case_exec_id = '%s' " \
                      % (self.safe(kwargs['case_id']), AbstractLog.START_STATUS,
                         self.safe(kwargs['case_exec_id']))
                cursor.execute(sql)
                if kwargs['exec_batch_id'] and kwargs['exec_batch_id'] !="" and kwargs['exec_batch_id'] != 0:
                    sql = "update case_exec_log set exec_batch_id='%s'" % self.safe(kwargs['exec_batch_id'])
                    cursor.execute(sql)

                if kwargs['machine_id'] and kwargs['machine_id'] != "":
                    sql = "update case_exec_log set machine='%s'" % self.safe(kwargs['machine_id'])
                    cursor.execute(sql)

                if kwargs['env_id'] and kwargs['env_id'] != "":
                    sql = "update case_exec_log set env='%s'" % self.safe(kwargs['env_id'])
                    cursor.execute(sql)

                if kwargs['product_id'] and kwargs['product_id'] != "":
                    sql = "update case_exec_log set product_id='%s'" % self.safe(kwargs['product_id'])
                    cursor.execute(sql)


                self.log.warn("删除case_oper_log的原有操作")
                sql = "delete from case_oper_log where case_exec_id=%s and case_id=%s" % (kwargs['case_exec_id'], kwargs['case_id'])
                self.log.debug("删除原有的case操作记录：%s" % sql)
                cursor.execute(sql)

                self._conn.commit()

    def update_case_exec_log(self, case_exec_id, status, fail_reason=''):
        sql = '''update case_exec_log set status = %d, end_time = now(), fail_reason = '%s' where case_exec_id = %d''' \
              % (int(status), self.safe(fail_reason), case_exec_id)
        with self._conn.cursor() as cursor:
            cursor.execute(sql)
            self._conn.commit()

    def start_plan_exec_log(self):
        with self._conn.cursor() as cursor:
            if self.testplan.plan_batch_id is None and self.testplan.exec_batch_id is None:
                now_date_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                self.testplan.plan_batch_id = "%s_%s%d" % (self.testplan.plan_id,
                                                           now_date_str, random.randint(100,999))
                self.testplan.exec_batch_id = "%s%d" % (now_date_str, random.randint(100, 999))
                sql = "INSERT INTO plan_exec_log VALUES (null, '%s', '%s', '%s', '%s', '%s', " \
                      "now(), NULL , '1', '%s', '%s', '1', null)" \
                      % (self.testplan.plan_batch_id, self.testplan.plan_id, self.testplan.plan_name,
                          self.testplan.exec_batch_id, self.testplan.machine_id, self.testplan.env_id,
                          self.testplan.product_id)
                cursor.execute(sql)
                self._conn.commit()

    def update_plan_exc_log(self, status):
        with self._conn.cursor() as cursor:
            sql = "update plan_exec_log set status = '%s', end_time = now() where exec_batch_id = '%s' and plan_batch_id = '%s'"\
                    % (status, self.testplan.exec_batch_id, self.testplan.plan_batch_id)
            self.log.debug("更新计划数据: %s" % sql)
            cursor.execute(sql)
            self._conn.commit()

    def step_log_before(self, oper_type, oper_name, oper_id, parent_oper_id=None, *key, **kwargs):
        SimpleLog.step_log_before(self, oper_type, oper_name, oper_id, parent_oper_id, *key, **kwargs)
        if oper_type == AbstractLog.STEP_TYPE_COMPONENT:
            self.add_case_oper_log(
                oper_type=AbstractLog.STEP_TYPE_STEP,
                oper_name=oper_name,
                component_id=oper_id,
                value="",
                operator="",
                expect_value="",
                case_id=self.testcase.case_id,
                case_exec_id=self.testcase.case_exec_id,
                node_id="",
                result=AbstractLog.START_STATUS,
                log_content="开始执行"
            )

    def step_log_after(self, oper_type, oper_name, oper_id, oper_time, result, log_content, parent_oper_id=None, *key,
                       **kwargs):
        SimpleLog.step_log_after(self, oper_type, oper_name, oper_id, oper_time, result, log_content, parent_oper_id,
                                 *key,
                                 **kwargs)
        self.add_case_oper_log(
            oper_type=oper_type,
            oper_name=oper_name,
            component_id=oper_id,
            value="",
            operator="",
            expect_value="",
            case_id=self.testcase.case_id,
            case_exec_id=self.testcase.case_exec_id,
            node_id="",
            result=result,
            log_content=log_content
        )

    def case_log_before(self, *key, **kwargs):
        SimpleLog.case_log_before(self, *key, **kwargs)
        self.start_case_exec_log(
            case_exec_id=self.testcase.case_exec_id,
            case_id=self.testcase.case_id,
            module_id=self.testcase.module_id,
            exec_batch_id=self.testplan.exec_batch_id,
            machine_id=self.testplan.machine_id,
            env_id=self.testplan.env_id,
            product_id=self.testplan.product_id
        )

    def case_log_after(self, result, run_time, log_content, *key, **kwargs):
        SimpleLog.case_log_after(self, result, run_time, log_content, *key, **kwargs)
        self.update_case_exec_log(self.testcase.case_exec_id, result, log_content)

    def plan_log_before(self, *key, **kwargs):
        SimpleLog.plan_log_before(self, *key, **kwargs)
        self.start_plan_exec_log()

    def plan_log_after(self, *key, **kwargs):
        SimpleLog.plan_log_after(self, *key, **kwargs)
        self.update_plan_exc_log(AbstractLog.SUCCESS_STATUS)
        self.disconnect()

    def disconnection(self):
        if self._conn is not None:
            self._conn.close()
