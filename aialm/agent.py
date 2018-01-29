# coding:utf-8
from aiautomation.agent.agent import Agent
from aiautomation.utils.config import Config
import sys
import os
sys.path.insert(0, os.getcwd() + "/../")

config = Config("./config.yml")

agent = Agent(config)
agent.report_timer_thread_start()
agent.start_task_receive()
