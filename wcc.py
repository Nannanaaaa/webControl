# -*-coding:utf-8 -*-

import time
import sys
from util.excutor import executor
from util.configReader import configReader
from util.DataBaseManager import DataBaseManager
from util.getMsg import getMsg

reload(sys)
sys.setdefaultencoding('utf-8')


class WCC(object):
    CONFIGPATH = '_config.ini'
    KEY_COMMAND = 'Command'
    KEY_OPEN = 'Open'
    KEY_Server = 'Server'
    KEY_Client = 'Client'
    KEY_TIMELIMIT = 'timelimit'

    def __init__(self):
        self.configReader = configReader(self.CONFIGPATH)
        self.initEnv()
        self.toRun()

    def initEnv(self):
        commandDict = self.configReader.getDict(self.KEY_COMMAND)
        openDict = self.configReader.getDict(self.KEY_OPEN)
        server = self.configReader.getDict(self.KEY_Server)
        print 'Server is: %s' % str(server)
        self.timeLimit = int(self.configReader.readConfig(self.KEY_Client, self.KEY_TIMELIMIT))
        self.excutor = executor(commandDict, openDict)
        self.dbManager = DataBaseManager(server['host'], int(server['port']))
        print 'init finished'

    def toRun(self):
        while True:
            print 'try:'
            self.run()
            time.sleep(self.timeLimit)

    def run(self):
        commandList = self._generateCommandList()
        print 'commandList is: %s' % str(commandList)
        if commandList:
            finishCommandList = self.excutor.execute(commandList)
            self.flagFinish(finishCommandList)

    def flagFinish(self, commandList):
        for each in commandList:
            self.dbManager.update(each, 'run', True)

    def _generateCommandList(self):
        commandObj = self.dbManager.find('run', False)
        ipobj = getMsg()
        myip = ipobj.getWebip()
        # myhostname = ipobj.getHostname()
        myiplan = ipobj.getLanip()
        commandList = []
        commandListTemp = []
        if commandObj:
            for each in commandObj:
                if each['ip'] == myip and each['iplan'] == myiplan:
                    commandListTemp.append(each)
        if commandListTemp:
            print 'in command obj'
            for each in commandListTemp:
                commandDict = {'_id': each['_id'],
                               'innerCommand': each['innerCommand'],
                               'writeCommand': each['writeCommand'],
                               'run': each['run']}
                commandList.append(commandDict)
            return commandList[::-1]  # 将列表倒序


if __name__ == '__main__':
# 1    
# 2
# 3
    mcc = WCC()
