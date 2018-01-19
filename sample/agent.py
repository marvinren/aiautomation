# coding:utf-8
from aiautomation.agent.agent import Agent
from aiautomation.utils.config import Config

config = Config("./config.yml")

agent = Agent(config)
agent.report_timer_thread_start()
agent.start_task_receive()