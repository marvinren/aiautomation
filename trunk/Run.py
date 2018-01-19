# -*- coding: UTF-8 -*-

from ObjectAction import *
import os
import logging
import platform
import Assert

print platform.system()
print os.path.sep

# 初始化配置
init_config('.')
# 初始化数据库
init_db()
logging.info(sys.argv)

# 获取python脚本名称
file_name = str(sys.argv[1])
# file_name = '/Users/reinhart/PycharmProjects/aicp_ui/case/102091_1118268.py'
# file_name = 'Y:\\PycharmProjects\\aicp_ui\\case\\1001_9003.py'

# 获取case信息
t_path = os.path.split(file_name)
logging.info(t_path)
tmp = t_path[1].split('.')[0]
case_id = int(tmp.split('_')[0])
case_exec_id = int(tmp.split('_')[1])

# 初始化case信息
logging.info('case_id:' + str(case_id))
set_case_id(case_id)
logging.info('case_exec_id:' + str(case_exec_id))
set_case_exec_id(case_exec_id)

try:
    # 判断脚本是否存在
    logging.info('file_name:' + file_name)
    if not os.path.isfile(file_name):
        # close_url()
        case_exec_finsh(11, '未找到指定脚本:' + file_name)
    else:
        try:
            # 初始化浏览器
            init_driver()

            # 执行脚本
            execfile(file_name)
            close_url()
            case_exec_finsh()
            logging.info('脚本执行成功!')
        except WebDriverException, ex:
            logging.error('脚本执行失败!:' + ex.msg)
            add_oper_log('ERROR', ex.msg)
            close_url()
            case_exec_finsh(11, '脚本执行失败!:' + ex.msg)
        except Exception, ex:
            logging.error('脚本执行失败!:' + ex.message)
            add_oper_log('ERROR', ex.message)
            close_url()
            case_exec_finsh(11, '脚本执行失败!:' + ex.message)
except Exception, ex:
    logging.error('脚本执行失败!:' + ex.message)
    case_exec_finsh(11, '脚本执行失败!:' + ex.message)
