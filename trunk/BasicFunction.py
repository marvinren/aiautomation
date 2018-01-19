# -*- coding: UTF-8 -*-

import ConfigParser
import logging
from email.header import Header
from email.utils import parseaddr, formataddr
import os

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='./logs/ui.log',
                    filemode='w')
CONFIG = {}


class MyConf(ConfigParser.ConfigParser):
    def __init__(self, defaults=None):
        ConfigParser.ConfigParser.__init__(self, defaults=None)

    def optionxform(self, optionstr):
        return optionstr


def format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))


def init_config(path):
    logging.info('config path:' + path)
    global CONFIG
    # tmpPath = inPath + '\\config.ini'
    c_path = path + '/config.ini'
    cf = MyConf()
    cf.read(c_path)
    for i in cf.sections():
        datas = cf.items(i)
        for tmpV in datas:
            CONFIG[tmpV[0]] = tmpV[1]
    CONFIG['path'] = path
    CONFIG['curFrames'] = []
    CONFIG['curCaseFile'] = ''
    for (d, v) in CONFIG.items():
        try:
            CONFIG[d] = int(v)
        except:
            pass
            # tmpPath = CONFIG['ora_path'] + '\\oraocci11.dll'
            # if os.path.exists(tmpPath):
            #     print 'cx_Oracle add success!'
            #     os.environ['PATH'] = CONFIG['ora_path'] + ';' + CONFIG['ora_path'] + '\\bin;' + os.environ['PATH']
            #     os.environ['TNS_ADMIN'] = CONFIG['ora_path']
            #     os.environ['ORACLE_HOME'] = CONFIG['ora_path']
            #     os.environ['NLA_LANG'] = "SIMPLIFIED CHINESE_CHINA.UTF8"
            # else:
            #     print 'cx_Oracle not added'
