# coding:utf-8
import json

import _thread
import threading
import traceback

import pika
import psutil
import socket

import time

import sys

from aiautomation.log.abstract_log import AbstractLog
from aiautomation.testcase.test_plan import PlanInfo, TestPlanRunner
from aiautomation.utils.log import get_logger

log = get_logger(__name__)


class ReportStateThread(threading.Thread):
    def __init__(self, agent):
        threading.Thread.__init__(self)
        self.agent = agent

    def run(self):
        agent = self.agent
        channel = agent.get_channel()
        while True:
            try:
                time.sleep(agent.report_delay)
                state = {"agent_id": agent.agent_id, "cpu": agent.get_cpu_state(),
                         "memory": agent.get_memory_state(),
                         "ip": agent.get_ip()}
                log.info("本机状态:%s" % state)
                channel.exchange_declare(exchange="agent_report", exchange_type="fanout")
                channel.basic_publish(exchange="agent_report", routing_key='', body=json.dumps(state),
                                      properties=pika.BasicProperties(content_type='application/json'))
            except Exception as ex:
                log.error("上报状态失败，错误：%r" % ex)


class Agent():
    def __init__(self, config=None):
        self.config = config

        self._agent_id = config.getConfig().aiautomation.agent.agent_id
        self._mq_host = config.getConfig().aiautomation.agent.mq_host
        self._mq_port = config.getConfig().aiautomation.agent.mq_port
        self._mq_user = config.getConfig().aiautomation.agent.mq_user
        self._mq_pwd = str(config.getConfig().aiautomation.agent.mq_pwd)
        self._report_delay = config.getConfig().aiautomation.agent.report_delay

        self.plan_runner = TestPlanRunner()

    @property
    def agent_id(self):
        return self._agent_id

    @property
    def mq_host(self):
        return self._mq_host

    @property
    def mq_port(self):
        return self._mq_port

    @property
    def mq_user(self):
        return self._mq_user

    @property
    def report_delay(self):
        return self._report_delay

    @property
    def mq_pwd(self):
        return self.mq_pwd

    def get_channel(self):
        credentials = pika.PlainCredentials(self._mq_user, self._mq_pwd)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self._mq_host, port=int(self._mq_port),
                                      credentials=credentials))
        channel = connection.channel()
        return channel

    def get_cpu_state(self):
        return str(psutil.cpu_percent(1))

    def get_memory_state(self):
        return str(psutil.virtual_memory().percent)

    def get_ip(self):
        return socket.gethostbyname(socket.gethostname())

    def report_timer_thread_start(self):
        t = ReportStateThread(self)
        t.start()

    def start_task_receive(self):
        channel = self.get_channel()

        def on_request(ch, method, props, body):
            resp = {'status': 9, 'fail_reason': '', 'agent': self._agent_id}

            log.info("-----------------------the message has bean received. --------------------------\n %r" % body)

            dto = json.loads(body, encoding='UTF-8')
            # resp['case_id'] = str(dto['caseId'])
            resp['case_exec_id'] = str(dto['caseExecId'])

            project_base_path = self.config.getConfig().aiautomation.runner.project_base_path
            project_module_sys_in_list = list(filter(lambda x: x.startswith(project_base_path), sys.modules.keys()))
            for module in project_module_sys_in_list:
                del sys.modules[module]


            try:
                print(str(dto['caseExecId']))
                self.plan_runner.run_case_by_case_exec_id(str(dto['caseExecId']), str(dto['caseId']))
                #resp['status'] = AbstractLog.SUCCESS_STATUS
            except Exception as e:
                resp['status'] = AbstractLog.ERROR_STATUS
                resp['fail_reason'] = str(e)
                log.error(traceback.format_exc())
                log.error(e)

            response = json.dumps(resp)

            channel.queue_declare(queue='case_finish', durable=True)
            channel.basic_publish(exchange='', routing_key='case_finish', body=response,
                                  properties=pika.BasicProperties(
                                      delivery_mode=2,  # make message persistent
                                      content_type='application/json'))

        queue_name = str(self._agent_id)
        channel.queue_declare(queue=queue_name, exclusive=True)

        # channel.basic_qos(prefetch_count=1)
        channel.basic_consume(on_request, queue=queue_name, no_ack=True)

        log.info(".............agent[%s] Awaiting RPC requests............." % queue_name)
        channel.start_consuming()
