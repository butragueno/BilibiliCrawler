import time
import os
import json
import threading
loglock = threading.Lock()

class log():
    def __init__(self):
        self.logValue = {}
        self.logValue['ipCount'] = 0
        self.logValue['userCount'] = 0
        self.logValue['videolistCount'] = 0
        self.logValue['videoCount'] = 0
        self.logValue['userdataCount'] = 0
        self.logValue['videolistdataCount'] = 0
        self.logValue['videodataCount'] = 0
        self.logValue['seasonCount']=0
        self.logValue['episodeCount']=0
        self.logValue['seasondataCount']=0
        self.logValue['episodedataCount']=0
        self.logValue['time']=0.00

    def addValue(self, key,value=1):    #更改使用次数
        with loglock:
            self.logValue[key] += value

    def getValue(self, key):    #获取使用次数
        try:
            return self.logValue[key]
        except:
            print('Read'+key+'failed')

    def saveValues(self):   #本地保存本次日志
        timenow = time.strftime("%Y%m%d%H%M%S", time.localtime())
        try:
            os.mkdir('log')
        except FileExistsError:
            pass
        with open('log/'+str(timenow)+' log.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.logValue))

lognow=log()

if __name__ == '__main__':
    a = log()
    a.saveValues()
    pass
