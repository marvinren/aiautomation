from aiautomation.log.simple_log import SimpleLog
from aiautomation.utils.config import Config
from sample.case.需求录入 import 需求录入
from sample.case.需求查询 import 需求查询
from sample.recovery.aialm_recovery import AialmRecovery

logger = SimpleLog()
config = Config("./config.yml")
recovery = AialmRecovery(logger, config)

# # 需求查询
# data = {"需求名称": "测试工时统计"}
# 需求查询(scenarios_recovery=recovery, logger=logger, config=config).测试案例1(data)
# 需求查询(scenarios_recovery=recovery, logger=logger, config=config).测试案例2(data)

# 需求录入
data = {}
需求录入(scenarios_recovery=recovery, logger=logger, config=config).普通需求录入(data)
