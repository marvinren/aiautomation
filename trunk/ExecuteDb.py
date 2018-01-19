# -*- coding: UTF-8 -*-

import logging
from DBpool import *
from BasicFunction import *


class ExecuteDb(object):
    """
    执行过程中数据生成与沉淀
    """

    def __init__(self):
        # 实例化数据库连接，统一使用
        self.DB = DBSql(CONFIG['db_con_str'])

    # 执行入库等funs:
    def get_element(self, name):
        """
        获取元素信息
        :param name: 元素名称
        :return:
        """
        sql = "select a.locator,a.locator_type from element_def a where a.element_name = '" + safe(name) + "'"
        # sql = ""
        e = self.DB.get_sql_list(sql, 1)
        return e

    def add_node_log(self, dict_params):
        """
        新增节点操作日志
        :param dict_params:
        :return:
        """
        sql = '''insert into case_oper_log (oper_type, oper_name, value, operator, expect_value, 
              oper_time, case_id, case_exec_id, node_id, component_id)
              values ('%s','%s','%s','%s','%s',now(), %d, %d, %d, %d )''' \
              % (safe(dict_params['oper_type']), safe(dict_params['oper_name']), safe(dict_params['value']),
                 safe(dict_params['operator']), safe(dict_params['expect_value']), dict_params['case_id'],
                 dict_params['case_exec_id'], dict_params['node_id'], dict_params['component_id'])
        self.DB.update(sql)

    def update_case_exec_status(self, case_exec_id, status, fail_reason=''):
        """
        更新用例执行完成时的状态
        :param case_exec_id:
        :param status:
        :param fail_reason:
        :return:
        """
        sql = '''update case_exec_log set status = %d, end_time = now(), fail_reason = '%s' where case_exec_id = %d''' \
              % (status, safe(fail_reason), case_exec_id)
        self.DB.update(sql)

        # # 更新符合用例状态(由Case模块统一处理)
        # sql = ''' select a.parent_exec_id,a.parent_case_id from case_exec_log a where a.case_exec_id = %d ''' \
        #       % case_exec_id
        # result = self.DB.get_sql_list(sql, 1)
        # if result and len(result) > 0:
        #     parent_exec_id = int(result[0][0])
        #     parent_case_id = int(result[0][1])
        #     if parent_exec_id > 0:
        #         # 判断父用例下其它用例的执行状况
        #         sql = '''select SUM(case when status = 10 then cnt else 0 end) suc_cnt,
        #         SUM(case when status = 11 then cnt else 0 end) fail_cnt,
        #         SUM(case when status = 0 then cnt else 0 end) idle_cnt,
        #         SUM(case when status = 1 then cnt else 0 end) work_cnt,
        #         SUM(case when status is null then cnt else 0 end) null_cnt
        #         FROM
        #         (
        #         select status,count(*) cnt from
        #         (
        #         select b.status from case_def a
        #         left join case_exec_log b
        #         on b.parent_case_id = a.parent_id and b.parent_exec_id = %d and a.case_id = b.case_id
        #         where a.parent_id = %d
        #         ) c group by status
        #         ) d''' % (parent_exec_id, parent_case_id)
        #         c = self.DB.get_sql_list(sql)
        #
        #         if c and len(c) > 0:
        #             suc_cnt = int(c[0][0])
        #             fail_cnt = int(c[0][1])
        #             idle_cnt = int(c[0][2])
        #             work_cnt = int(c[0][3])
        #             null_cnt = int(c[0][4])
        #
        #             if idle_cnt > 0 or work_cnt > 0 or null_cnt > 0:
        #                 logging.info('复合用例[' + str(parent_case_id) + ']还未执行完成!')
        #                 return
        #             elif fail_cnt > 0:
        #                 logging.info('复合用例[' + str(parent_case_id) + ']执行失败!')
        #                 st = 11
        #             else:
        #                 logging.info('复合用例[' + str(parent_case_id) + ']执行成功!')
        #                 st = 10
        #
        #             sql = '''update case_exec_log set status = %d, end_time = now() where case_exec_id = %d  ''' \
        #                   % (st, parent_exec_id)
        #             self.DB.update(sql)


def safe(s):
    return MySQLdb.escape_string(str(s))
