import pymysql
from aiautomation.log.simple_log import SimpleLog


class AiciResultLog(SimpleLog):
    """
        向数据库写入结果，但是使用的是单connection，可以考虑做一个数据库连接池
    """

    START_STATUS = 0
    SUCCESS_STATUS = 10
    ERROR_STATUS = 11

    def __init__(self, config=None):
        SimpleLog.__init__(self)
        if config is None:
            raise AttributeError("AiciResultLog请注入config对象")
        self._url = config.getConfig().aiautomation.agent.db_url
        self._port = config.getConfig().aiautomation.agent.db_port
        self._user = config.getConfig().aiautomation.agent.db_user
        self._pwd = config.getConfig().aiautomation.agent.db_pwd

        self._conn = pymysql.connect(host='10.12.1.23', port=3306, user='root', passwd='Yijiceshi4!',
                                     db='autotest', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    def disconnect(self):
        if self._conn is not None:
            self._conn.close()

    def safe(self, parameter):
        return pymysql.escape_string(str(parameter))

    def add_case_oper_log(self, **kwargs):
        sql = "insert into case_oper_log (oper_type, oper_name, value, operator, expect_value, oper_time, case_id, case_exec_id, node_id, component_id) " \
              "values ('%s','%s','%s','%s','%s',now(), %d, %d, %d, %d )" \
              % (self.safe(kwargs['oper_type']), self.safe(kwargs['oper_name']), self.safe(kwargs['value']),
                 self.safe(kwargs['operator']), self.safe(kwargs['expect_value']), self.kwargs['case_id'],
                 kwargs['case_exec_id'], self.kwargs['node_id'], self.kwargs['component_id'])
        with self._conn.cursor() as cursor:
            cursor.execute(sql)
            self._conn.commit()

    def start_case_exec_log(self, **kwargs):
        sql = "INSERT INTO case_exec_log VALUES ('%s', '0', '%s', 'SINGLE', '0', null, null, '%s', " \
              "'%s', null, null, null, '%s', null, " \
              "now(), null, '%s', '%s', '%s', null)" \
              % (self.safe(kwargs['case_exec_id']), self.safe(kwargs['case_id']), self.safe(kwargs['exec_batch_id']),
                 self.saft(kwargs['result']), self.safe(kwargs['log_content']), self.saft(kwargs['machine_id']),
                 self.safe(kwargs['env_id']), self.safe(kwargs['product_id']))
        with self._conn.cursor() as cursor:
            cursor.execute(sql)
            self._conn.commit()

    def update_case_exec_log(self, case_exec_id, status, fail_reason=''):
        sql = '''update case_exec_log set status = %d, end_time = now(), fail_reason = '%s' where case_exec_id = %d''' \
              % (status, self.safe(fail_reason), case_exec_id)
        with self._conn.cursor() as cursor:
            cursor.execute(sql)
            self._conn.commit()

    def before_case_log(self, case_id, case_exec_id, node_id, case_name, module_name, *key, **kwargs):
        SimpleLog.before_case_log(case_id, case_exec_id, node_id, case_name, module_name, *key, **kwargs)
        self.start_case_exec_log(case_id=case_id, case_exec_id=case_exec_id, node_id=node_id, case_name=case_name,
                            module_name=module_name, result='0', log_content='开始执行....')
