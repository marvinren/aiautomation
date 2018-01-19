# coding=utf-8
import time

import datetime


class Report(object):
    """
    此为报告的基类，用于抽象出报告的公共部分，其他报告类均继承此类
    """
    cLogFile = ""  # log文件路径

    def __init__(self):
        super(Report, self).__init__()

    @staticmethod
    def getCurrentTime(in_format='%Y-%m-%d %H:%M:%S'):
        """
        根据inFormat得到当前时间的字符串
        :param inFormat:时间格式，如：yyyy-MM-dd HH:mm:ss
        :return (str) 按照时间格式生成字符串
        """

        return time.strftime(in_format, time.localtime(time.time()))

    @staticmethod
    def caluTimeSlice(inStartTime, inEndTime):
        """
        计算时间差
        :param inStartTime: 开始时间
        :param inEndTime: 结束时间
        :return: 时间差，整型变量
        """
        return datetime.datetime.strptime(inEndTime, "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(inStartTime,
                                                                                                       "%Y-%m-%d %H:%M:%S")

    @staticmethod
    def writeLog(inMsg):
        """
        写入日志内容
        :param inMsg:日志的内容
        :return 1 or 0
        """
        try:
            Report.openLog()
            with open(Report.cLogFile, 'a') as filelog:
                inMsg += "\n"
                filelog.write(inMsg)
        except Exception, e:
            print e
        return 1

    @staticmethod
    def openLog():
        """
        打开日志文件
        :return 1或0，成功或失败
        """
        try:
            if Report.cLogFile == "":
                Report.cLogFile = "logs/steps.txt"
                Report.writeLog("[" + Report.getCurrentTime("%Y-%m-%d %H:%M:%S") + "]@Log@打开 log 文件")
        except Exception, e:
            print e
        return 1

        # s=Report()
        # s.writeLog("1")
        # s.writeLog("12")
        # s.writeLog("123")
        # s.writeLog("1234")
        # p=s.caluTimeSlice("2016-08-24 10:53:08","2017-08-24 10:53:09")
        # print p
