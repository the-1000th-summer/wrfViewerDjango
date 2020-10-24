""" 此文件用于解析rsl.out.0000文件 """

from datetime import datetime
# import matplotlib.pyplot as plt

class rslOutParser:
    """ 此类用于解析rsl.out.0000文件 """

    def __init__(self, rslFilePath):
        self.rslFilePath = rslFilePath
        self.dataLines = []

    def tryParse(self):
        """ a """
        print('aaaaa')
        with open(self.rslFilePath) as rslFile:
            self.dataLines = rslFile.readlines()
        # print(dataLines[:10])
        
        host = self.getHostRunningIn()
        cores = self.getCoresRunning()
        dateTimes, elapseSecs = self.getAllTime()

        # '%F %X 格式示例：2016-01-01 00:00:18'
        outData = {
            'host': host,
            'cores': cores,
            'dateTimes': [eachDateTime.strftime('%F %X') for eachDateTime in dateTimes],
            'elapseSecs': elapseSecs
        }

        # print('hahahaha', aa)
        # return str(aa)
        # return self.getDataLineNowTimeAndElapsedSec(firstIndex)
        return outData

    def getHostRunningIn(self):
        """ 此方法获取WRF在哪个主机上运行 """
        keyStr = 'hostname: '
        firstLine = self.dataLines[0]
        if keyStr in firstLine:
            return firstLine[firstLine.index(keyStr) + len(keyStr):].strip()
        else:
            return 'None'

    def getCoresRunning(self):
        """ 此方法获取用了几个核跑WRF """
        thirdLineWords = self.dataLines[2].split()
        x, y = thirdLineWords[3], thirdLineWords[-1]
        try:
            cores = int(x) * int(y)
        except ValueError:
            return 'unknown: parse error'
        return cores

    def findStartRunningIndex(self):
        """ 此方法找出第一行Timing for main:... """
        startCalIndex = 0
        headingStr = 'Timing for main:'
        while startCalIndex < len(self.dataLines):
            nowDataLine = self.dataLines[startCalIndex]
            if headingStr in nowDataLine and nowDataLine.index(headingStr) == 0:
                return startCalIndex
            startCalIndex += 1
        return 'None'
    
    def getAllTime(self):
        """_"""
        nowLineIndex = self.findStartRunningIndex()
        firstDateTime, _, _ = self.getDataLineNowTimeDomainAndElapsedSec(nowLineIndex)
        if firstDateTime is None:
            return [], []

        dateTimes, elapseSecs = [], []
        while nowLineIndex < len(self.dataLines):
            nowDateTime, nowDomain, nowElapseSec = self.getDataLineNowTimeDomainAndElapsedSec(nowLineIndex)
            if nowDateTime is None:
                nowLineIndex += 1
                continue
            dateTimes.append(nowDateTime)
            elapseSecs.append(nowElapseSec)
            nowLineIndex += 1

        # print(len(dateTimes), len(elapseSecs))
        
        return dateTimes, elapseSecs

    def getDataLineNowTimeDomainAndElapsedSec(self, lineIndex):
        """ 此方法获取一行log内的当前时间和运算时长 """
        dataLineWords = self.dataLines[lineIndex].split()
        try:
            nowDateTime = datetime.strptime(dataLineWords[4], '%Y-%m-%d_%H:%M:%S')
            domain = int(dataLineWords[-4][:-1])
            elapseSec = float(dataLineWords[-3])
        except ValueError:
            return None, None, None
        return nowDateTime, domain, elapseSec

