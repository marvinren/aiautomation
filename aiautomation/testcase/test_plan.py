import csv
import sys
import traceback
from functools import wraps

from aiautomation.testcase.test_case_generator import TestcaseGenerator
from aiautomation.utils.config import Config
from aiautomation.utils.load_helper import import_object
from aiautomation.utils.log import get_logger

log = get_logger(__name__)


def plan_run(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        ret = None
        logger = args[0].logger
        try:
            logger.plan_log_before()
            ret = func(*args, **kwargs)
        finally:
            logger.plan_log_after()
            return ret

    return wrap


class PlanInfo:

    def __init__(self, plan_id, plan_name, plan_batch_id, exec_batch_id, env_id, machine_id, plan_data_id, product_id):
        self.plan_id = plan_id
        self.plan_name = plan_name
        self.plan_batch_id = plan_batch_id
        self.exec_batch_id = exec_batch_id
        self.env_id = env_id
        self.machine_id = machine_id
        self.plan_data_id = plan_data_id
        self.product_id = product_id


class TestPlan:
    pass


class TestPlanRunner:

    def __init__(self, config_file="./config.yml", plan=None):
        self._config = Config(config_file).getConfig()
        self._plan = plan
        self._logger = None
        self._recovery = None
        self._project_case_path = None

        self.load_logger()
        self.load_recovery()
        self.check_plan()
        self.inject_plan_to_logger()
        self.set_project_case_path()

        self.module_list = {}
        self.case_list = []

    @property
    def logger(self):
        return self._logger

    def add_case(self, module_name, case_name, data=None):
        if data is not None and isinstance(data, str):
            csv_reader = csv.reader(open(data, encoding='utf-8'))
            cols = None
            for row in csv_reader:
                if cols is None:
                    cols = row
                    continue
                data = {}
                for index in range(0, len(cols)):
                    data[cols[index]] = row[index]
                print(data)
                self.case_list.append({"module_name": module_name, "case_name": case_name, "data": data})
        else:
            self.case_list.append({"module_name": module_name, "case_name": case_name, "data": data})

    def simple_run(self, module_name, case_name, data=None):
        module_obj = import_object("%s.%s.%s" % (self._project_case_path, module_name, module_name),
                                   scenarios_recovery=self._recovery, logger=self._logger, config=self._config)
        case_method = getattr(module_obj, case_name)
        return case_method(data)

    def run_case_by_case_exec_id(self, case_exec_id, case_id):
        tg = TestcaseGenerator(config=self._config)
        try:
            tg.connection()
            tg.generate_case_by_case_ids(case_id, case_exec_id)
            names = tg.fetch_case_name_module_name(case_id)
        finally:
            tg.disconnection()
        print(names)
        self.simple_run(names['group_name'], names['case_name'])

    def agent_run(self, case_id, case_exec_id, module_id, script_str):
        file_name = "./cases/module_%s_%s.py" % (case_id, case_exec_id)
        module_name = "module_%s_%s" % (case_id, case_exec_id)
        case_name = "case_%s_%s" % (case_id, case_exec_id)
        script = """
# -*- coding: UTF-8 -*-
from aiautomation.testcase.decorator import testcase
from aiautomation.testcase.test_case_module import TestCaseModule


class %s(TestCaseModule):

    @testcase(case_id=%s, case_exec_id=%s, module_id=%s)
    def %s(self, data=None): 
%s           
""" % (module_name, case_id, case_exec_id, module_id, case_name, "\n".join(list(map(lambda x: "\t\t%s" % x, script_str.split("\n")))))

        with open(file_name, "w") as file:
            file.write(script)
            # file.write("\n")
            # for line in script_str.split("\n"):
            #     file.write("\t\t%s\n" % line)
        self.simple_run(module_name, case_name)

    @plan_run
    def start(self):
        for case in self.case_list:
            self.simple_run(case['module_name'], case['case_name'], case['data'])

    def load_logger(self):
        try:
            import_str = self._config.aiautomation.logger.class_name
            mod_str, _sep, class_str = import_str.rpartition('.')
            __import__(mod_str)
            logger_class = getattr(sys.modules[mod_str], class_str)
            self._logger = logger_class(config=self._config)

        except Exception as e:
            log.error("请查看配置文件中的aiautomation.logger.class_name是否配置正确，可配置如：aiautomation.log.simple_log.SimpleLog")
            log.error(traceback.format_exc())
            raise ValueError("aiautomation.logger")

    def load_recovery(self):
        import_str = None
        try:
            import_str = self._config.aiautomation.runner.recovery.class_name
        except Exception as e:
            log.warn("请查看配置文件中的aiautomation.runner.recovery.class_name")
            # log.warn(traceback.format_exc())
        finally:
            if import_str is None:
                import_str = "recovery.recovery.Recovery"
                log.warn("场景回复路径暂时设置成:%s" % import_str)
            mod_str, _sep, class_str = import_str.rpartition('.')
            __import__(mod_str)
            recovery_class = getattr(sys.modules[mod_str], class_str)
            self._recovery = recovery_class(config=self._config, logger=self._logger)

    def set_project_case_path(self):
        try:
            self._project_case_path = self._config.aiautomation.runner.project_base_path + ".cases"
        except:
            log.warn("请查看配置文件中的aiautomation.runner.project_case_path， 工程路径设置为[cases]")
            self._project_case_path = "cases"

    def check_plan(self):
        if self._plan is None:
            self._plan = PlanInfo(0, "虚拟计划", 0, 0, 0, 0, 0, 0)
        self._logger.testplan = self._plan

    def inject_plan_to_logger(self):
        self._logger.testplan = self._plan

