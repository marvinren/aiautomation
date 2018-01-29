import codecs

import pymysql
import os

tab_str = "    "

case_module_template = '''# coding: utf-8
import time
from selenium.webdriver.common.by import By

from aiautomation.gui.page import Page
from aiautomation.testcase.decorator import component


class %s(Page):
%s

'''

component_template = '''
    @component(%s)
    def %s(self, data=None):
%s'''

case_case_template = '''# coding: utf-8

from aiautomation.testcase.decorator import testcase
from aiautomation.testcase.test_case_module import TestCaseModule


class %s(TestCaseModule):
%s
'''

case_template = '''
    @testcase(case_id=%d, module_id=%d, case_exec_id=%s)
    def %s(self, data=None):
%s
        
%s
'''


class TestcaseGenerator():

    def __init__(self, config):
        self._config = config
        # self.connection()

    def connection(self):
        if self._config is None:
            raise AttributeError("AiciResultLog请注入config对象")
        _host = self._config.aiautomation.agent.db_host
        _port = self._config.aiautomation.agent.db_port
        _user = self._config.aiautomation.agent.db_user
        _pwd = self._config.aiautomation.agent.db_pwd
        _dbname = self._config.aiautomation.agent.db_dbname
        self._conn = pymysql.connect(host=_host, port=_port, user=_user, passwd=_pwd,
                                     db=_dbname, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    def disconnection(self):
        if self._conn is not None:
            self._conn.close()

    def fetch_all_modules_by_case_id(self, case_ids):
        with self._conn.cursor() as cursor:
            if not isinstance(case_ids, list):
                case_id_list = case_ids
            else:
                case_id_list = ",".join(case_ids)
            sql = "select distinct co.fun_id from case_node cc, case_def ca, component_def co " \
                  "where cc.case_id = ca.case_id and cc.component_id = co.component_id and ca.case_id in (%s)" % case_id_list

            cursor.execute(sql)
            result = cursor.fetchall()
            fun_id_list = list(map(lambda o: o['fun_id'], result))
            return fun_id_list

    def write_pages(self, module_path, case_ids):

        fun_id_list = self.fetch_all_modules_by_case_id(case_ids)
        with self._conn.cursor() as cursor:
            for fun_id in fun_id_list:

                component_scripts = []

                sql = "select component_id, component_name, script from component_def where fun_id = %d" % fun_id
                cursor.execute(sql)
                components = cursor.fetchall()
                for component in components:
                    script = "".join(
                        list(map(lambda line: "%s%s%s\n" % (tab_str, tab_str, line), component['script'].split("\n"))))
                    function_script = component_template % (
                        component['component_id'], component['component_name'], script)
                    component_scripts.append(function_script)

                sql = "select group_name from group_def where group_id = %d" % fun_id
                cursor.execute(sql)
                result = cursor.fetchone()
                module_name = result['group_name']
                module_script = case_module_template % (module_name, ("".join(component_scripts)))

                module_file_name = module_path + "/" + module_name + ".py"
                if not os.path.exists(module_path):
                    os.mkdir(module_path)
                codecs.open(module_file_name, "w", "utf8").write(module_script)

    def fetch_all_case_module(self, case_ids):
        if not isinstance(case_ids, list):
            case_id_list = case_ids
        else:
            case_id_list = ",".join(case_ids)

        with self._conn.cursor() as cursor:
            sql = "select distinct gd.group_id, gd.group_name from case_def cd, group_def gd " \
                  "where cd.case_group_id = gd.group_id and cd.case_id in (%s)" % case_id_list
            cursor.execute(sql)

            result = cursor.fetchall()
            group_id_list = list(map(lambda o: o['group_id'], result))

            return group_id_list

    def write_case(self, case_path, case_ids, case_exec_ids=None):
        group_id_list = self.fetch_all_case_module(case_ids)
        if not isinstance(case_exec_ids, list):
            case_exec_ids = [str(case_exec_ids)]

        with self._conn.cursor() as cursor:
            for group_id in group_id_list:
                if case_exec_ids is None:
                    sql = "select case_id, 0 case_exec_id, case_name, case_group_id from case_def where case_group_id = %d" % group_id
                else:
                    sql = "select cd.case_id, cel.case_exec_id, cd.case_name, cd.case_group_id from case_def cd, case_exec_log cel" \
                          " where cd.case_id = cel.case_id and cd.case_group_id = %d and cel.case_exec_id in (%s)" \
                          % (group_id, ",".join(case_exec_ids))
                cursor.execute(sql)
                cases = cursor.fetchall()
                if cases is None or len(cases) <= 0:
                    raise Exception("没找到相关测试案例")

                cases_scripts = []
                for case in cases:
                    sql = "select cod.component_name, gd.group_name from case_def cad, case_node cn, component_def cod, group_def gd " \
                          "where cad.case_id = cn.case_id and cn.component_id = cod.component_id and gd.group_id = cod.fun_id " \
                          "and cad.case_id = %d order by cn.exec_order asc" % case['case_id']
                    cursor.execute(sql)
                    components = cursor.fetchall()

                    case_import_list = []
                    case_script_list = []
                    for component in components:
                        import_case = "%s%sfrom ..pages.%s import %s" % (
                            tab_str, tab_str, component['group_name'], component['group_name'])
                        if import_case not in case_import_list:
                            case_import_list.append(import_case)
                        case_script_list.append(
                            "%s%sself.create_page(%s).%s(data)" % (
                            tab_str, tab_str, component['group_name'], component['component_name']))

                    case_script = case_template % (
                        case['case_id'],
                        group_id,
                        case['case_exec_id'],
                        case['case_name'],
                        "\n".join(case_import_list),
                        "\n".join(case_script_list))

                    cases_scripts.append(case_script)

                sql = "select group_name from group_def where group_id = %d" % group_id
                cursor.execute(sql)
                group_name = cursor.fetchone()['group_name']

                case_module_str = case_case_template % (group_name, "\n\n".join(cases_scripts))

                if not os.path.exists(case_path):
                    os.mkdir(case_path)
                # open(case_path + "/%s.py" % group_name, "w").write(case_module_str)
                codecs.open(case_path + "/%s.py" % group_name, "w", "utf8").write(case_module_str)

    def generate_case_by_case_ids(self, case_ids, case_exec_ids=None):
        self.write_pages("./pages", case_ids)
        self.write_case("./cases", case_ids, case_exec_ids)

    def fetch_case_name_module_name(self, case_id):
        with self._conn.cursor() as cursor:
            sql = "select cd.case_name, gd.group_name from case_def cd, group_def gd where cd.case_group_id = gd.group_id and cd.case_id = %s" % case_id
            cursor.execute(sql)
            return cursor.fetchone()
