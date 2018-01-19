# -*- coding: UTF-8 -*-

import pika
import RunCase
import json
import thread
import psutil
import re
from subprocess import Popen, PIPE
import platform
import time
from Tasklet import Tasklet
import logging

from BasicFunction import *

connection = None
channel = None
queue_name = None
timer = None
agent_id = None


def init():
    global connection, channel, queue_name, agent_id

    # 初始化配置
    init_config('.')
    agent_id = str(CONFIG['agent_id'])

    # 建立rabbitmq连接
    credentials = pika.PlainCredentials(str(CONFIG['mq_user']), str(CONFIG['mq_pwd']))
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=str(CONFIG['mq_host']), port=int(CONFIG['mq_port']), credentials=credentials))
    channel = connection.channel()
    # queue_name = str(CONFIG['agent_id'])
    # channel.queue_declare(queue=queue_name, exclusive=True)


# 获取cpu使用率
def get_cpu_state():
    return str(psutil.cpu_percent(1))


# 获取内存使用率
def get_memory_state():
    return str(psutil.virtual_memory().percent)


# 获取本机活动IP
def get_ip():
    if platform.system() == 'Darwin':
        ip_list = []
        ip_list = re.findall('\d+\.\d+\.\d+\.\d+', Popen('ifconfig', stdout=PIPE).stdout.read())
        return ip_list[-2]
    else:
        return re.search('\d+\.\d+\.\d+\.\d+', Popen('ipconfig', stdout=PIPE).stdout.read()).group(0)


# 上报Agent状态
def report_state():
    while True:
        try:
            time.sleep(CONFIG['report_delay'])

            state = {"agent_id": str(CONFIG['agent_id']), "cpu": get_cpu_state(), "memory": get_memory_state(),
                     "ip": get_ip()}
            logging.info(state)

            channel.exchange_declare(exchange='agent_report',
                                     exchange_type='fanout')
            channel.basic_publish(exchange='agent_report',
                                  routing_key='',
                                  body=json.dumps(state),
                                  properties=pika.BasicProperties(
                                      content_type='application/json'
                                  ))
        except Exception, ex:
            logging.error("上报状态失败!原因: %r " % ex)


# 上报定时程序
def report_timer():
    # global timer
    # timer = threading.Timer(CONFIG['report_delay'], report_state)
    # timer.start()
    thread.start_new(report_state, ())


# 回调函数
def on_request(ch, method, props, body):
    resp = {'status': 9, 'fail_reason': '', 'agent': agent_id}

    logging.info(" .........message coming.........\n %r" % body)

    # 将消息转化成JSON对象
    dto = json.loads(body, encoding='UTF-8')
    resp['case_exec_id'] = str(dto['caseExecId'])
    timeout = None
    if dto['timeout']:
        timeout = int(dto['timeout'])

    try:
        exec_type = dto['execType']
        if not exec_type:
            exec_type = 'UI'

        # 生成脚本文件
        if 'UI'.__eq__(exec_type) or 'STRESS'.__eq__(exec_type):
            script = str(dto['uiScrpit'])
            file_path = CONFIG['case_path'] + os.path.sep + exec_type
            file_name = file_path + os.path.sep + str(dto['caseId']) + "_" + str(dto['caseExecId']) + ".py"
        else:
            raise BaseException('不支持的用例类型!')

        file_object = None
        try:
            if not os.path.exists(file_path):
                os.mkdir(file_path)
            file_object = open(file_name, 'w')
            file_object.write(script)
        except BaseException, ex:
            raise BaseException(" 生成脚本文件失败! 原因: %r" % ex.message)
        finally:
            if file_object:
                file_object.close()

        rtn = RunCase.run_case(file_name, timeout)
        if rtn:
            raise BaseException(rtn)
    except BaseException, ex:
        resp['status'] = 11
        resp['fail_reason'] = ex.message
        logging.error(ex.message)

    response = json.dumps(resp)

    channel.queue_declare(queue='case_finish', durable=True)
    channel.basic_publish(exchange='',
                          routing_key='case_finish',
                          body=response,
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                              content_type='application/json'
                          ))


# 开始监听queue
def start():
    # 建立rabbitmq连接
    credentials = pika.PlainCredentials(str(CONFIG['mq_user']), str(CONFIG['mq_pwd']))
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=str(CONFIG['mq_host']), port=int(CONFIG['mq_port']), credentials=credentials))
    channel = connection.channel()
    queue_name = str(CONFIG['agent_id'])
    channel.queue_declare(queue=queue_name, exclusive=True)

    # channel.basic_qos(prefetch_count=1)
    channel.basic_consume(on_request, queue=queue_name, no_ack=True)

    logging.info(".............agent[%s] Awaiting RPC requests............." % queue_name)
    channel.start_consuming()


if __name__ == '__main__':
    init()
    report_timer()
    start()
