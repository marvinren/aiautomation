# coding=utf-8
from Report import Report
from BasicFunction import *
import datetime


class StepReport(Report):
    """
    记录步骤信息, 步骤为用例不可分割的一部分
    """
    stepList = []  # 步骤表
    stepMatched = 0
    configLev = 3  # log级别

    def __init__(self):
        super(StepReport, self).__init__()

    @staticmethod
    def AI_GetStepConfig(inStepCfg):
        """
                            解析字符串, 得到步骤的配置信息，根据配置信息进行输出
        :param inStepCfg:配置字符串
        :returns _vRe:字典
        """
        _vRe = {}
        if inStepCfg.upper() == 'NULL' or inStepCfg.upper() == "":
            _vRe.setdefault("stepname", "未指定")
            _vRe.setdefault("outputkey", "NULL")
            _vRe.setdefault("group", "1")
            return _vRe
        _vItems = inStepCfg.split(",")
        # 拆解
        try:
            for i in _vItems:
                _vKV = i.split(":")
                StepReport.AI_WriteLog("添加本步骤的配置信息[" + _vKV[0] + "],[" + _vKV[1] + "]到字典中", "Data", 2)
                _vRe.setdefault(_vKV[0], _vKV[1])
        except Exception, e:
            print e
            if len(_vRe) == 0:
                _vRe.setdefault("stepname", "未指定")
                _vRe.setdefault("outputkey", "NULL")
                _vRe.setdefault("group", "1")
        return _vRe

    @staticmethod
    def AI_WriteLog(inMsg, inLogType, inLogLev):
        """
        输出日志信息

        :param inMsg: 步骤信息的说明
        :param inLogType: 日志类型
        :param inLogLev: 输出log信息的等级，此方法用于控制log信息输出的规模,
                    信息级别包括:重要(0)、次级重要(1)、一般{2}、等
        :return:
        """
        # 写入日志
        if StepReport.configLev > inLogLev:
            vLogMsg1 = "[" + StepReport.getCurrentTime('%Y-%m-%d %H:%M:%S') + "]@" + inLogType + "@" + inMsg
            vLogMsg2 = "@" + inLogType + "@" + inMsg
            # print vLogMsg1
            # print vLogMsg2
            StepReport.writeLog(vLogMsg1)
            # Log.logInfo(vLogMsg2)
            pass

    @staticmethod
    def AI_PrintAtStepBegin(inMsg):
        """
                             步骤信息输出, 此函数为信息头。与PrintAtStepEnd为一组
        :param inMsg: 步骤信息的说明
        :return:
        """
        outMsg=inMsg+'<失败>'
        currentTime=StepReport.getCurrentTime("%Y-%m-%d %H:%M:%S")
        #默认异常发送的时间=当前时间+超时时间
        errorEndTime=datetime.datetime.strptime(currentTime,'%Y-%m-%d %H:%M:%S')+datetime.timedelta(seconds=CONFIG['TimeOut'])
        vStepMsg = StepReport.setStepMsg(currentTime, inMsg, outMsg, errorEndTime.strftime("%Y-%m-%d %H:%M:%S"), "0", "2")

        # 添加信息, 同时设定，如果大于1000，自动清理
        if len(StepReport.stepList) > 1000:
            StepReport.stepList = []

        StepReport.stepList.append(vStepMsg)
        StepReport.stepMatched = 1

        # 写入日志
        StepReport.AI_WriteLog_S("AI_PrintAtStepBegin@" + inMsg)

    @staticmethod
    def setStepMsg(inStartTime, inStepDesc, inStepOutput, inEndTime, inExecTime, inResult):
        """
        设置步骤信息，此函数用于步骤执行前
        :param  inStartTime:开始时间
        :param  inStepDesc:当前步骤的描述
        :param  inStepOutput:当前步骤的输出
        :param  inEndTime:结束时间
        :param  inExecTime:本次执行时间
        :param  inResult:本次执行结果
        :return 列表
        """
        return [inStartTime, inStepDesc, inStepOutput, inEndTime, inExecTime, inResult]

    @staticmethod
    def AI_WriteLog_S(inMsg):
        """
                             输出日志信息
        :param inMsg: 步骤信息的说明
        :return:
        """
        StepReport.AI_WriteLog(inMsg, "Log", 0)
    
    @staticmethod    
    def AI_PrintAtStepOutPut(inMsg):
        """
                            步骤信息输出,此函数为信息输出。插入在 PrintAtStepBegin 与 PrintAtStepEnd 间使用，可以有多个
        :param inMsg 步骤信息的说明
        """
        vCurIndex = len(StepReport.stepList) - 1
        
        if StepReport.stepMatched != 0:
            StepReport.stepList[vCurIndex][2] = inMsg
            StepReport.AI_WriteLog_S("AI_PrintAtStepOutPut@"+inMsg)
        else:
        
            StepReport.AI_PrintAtStepBegin("执行中发生了错误");
        

    @staticmethod
    def AI_PrintAtStepEnd_E(inMsg):
        """
        步骤信息输出, 此函数为信息尾。与PrintAtStepBegin为一组
        :param inMsg:
        :return:
        """
        StepReport.AI_PrintAtStepEnd(inMsg, "1")

    @staticmethod
    def AI_PrintAtStepEnd(inMsg, resultType):
        """
        :param inMsg:
        :param resultType: 1成功, 0未执行，其他表示失败
        :return:
        """
        if StepReport.stepMatched == 0:
            StepReport.AI_PrintAtStepBegin("执行中发生了错误")
        # 是否有输出
        if inMsg.upper() != '':
            StepReport.AI_PrintAtStepOutPut(inMsg)
        vCurIndex = len(StepReport.stepList) - 1
        # 结束时间
        StepReport.stepList[vCurIndex][3] = StepReport.getCurrentTime('%Y-%m-%d %H:%M:%S')
        StepReport.stepList[vCurIndex][4] = str(
            StepReport.caluTimeSlice(StepReport.stepList[vCurIndex][0], StepReport.stepList[vCurIndex][3]))
        StepReport.stepList[vCurIndex][5] = resultType
        StepReport.stepMatched = 0
        StepReport.AI_WriteLog_S("AI_PrintAtStepEnd@当前步骤结束,本次执行时间为:[" + StepReport.stepList[vCurIndex][4] + "]")

    @staticmethod
    def getStepList():
        """
        返回stepList
        :return: stepList
        """
        return StepReport.stepList

    @staticmethod
    def AI_ClearStepList():
        """
                           清除步骤
        :return:
        """
        StepReport.stepList[:] = []
