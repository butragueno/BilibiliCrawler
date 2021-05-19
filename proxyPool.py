import random
import requests
import json
import time
import threading
import log
proxylock = threading.Lock()

def createProxiesPool(size=10): #创建代理池并启动一个单独的线程运行维护程序
    def job():
        while True:
            maintainProxies(size)
            time.sleep(300)
    proxies=getProxies(size)
    saveProxies(proxies)
    a=threading.Thread(target=job)
    a.daemon=True
    a.start()

def invalidProxy(proxy):    #当程序调用代理但无法连接后将调用该函数将这个无效代理删除
    proxynew=proxy['http'][7:]
    proxies=loadProxies()
    for position in range(len(proxies)):
        i=proxies[position].count(proxynew)
        if i!=0:
            del proxies[position]
            break
    proxiesnew=getProxies(1)
    proxies+=proxiesnew
    saveProxies(proxies)

def maintainProxies(size):  #该程序将检查代理是否过期或者失效，之后将有问题的代理删除并加入新的代理
    def delProxy(proxies,position): #删除无效代理
        proxies.pop(position)
        return proxies
    def checkProxies(proxies):      #挨个检测代理
        proxiespositions=[]
        for x in range(len(proxies)):
            if isexpire(proxies[x])==True:
                proxiespositions.append(x)
            elif validate(proxies[x][0])==False:
                proxiespositions.append(x)
        return proxiespositions     #return a list
    def addProxies(proxies,size):   #多删少补
        if len(proxies)==size:
            return proxies
        elif len(proxies)<size:
            proxiesnew=getProxies(size-len(proxies))
            return proxies+proxiesnew
        else:
            more=len(proxies)-size
            for x in range(more):
                proxies=delProxy(proxies, 0)
            return proxies
    def isexpire(proxy):            #是否过期
        stamp=int(time.mktime(time.strptime(proxy[1], "%Y-%m-%d %H:%M:%S")))
        stampnow=time.time()
        if stampnow>=(stamp-300):
            return True        
        else:
            return False
    def validate(proxy):            #是否失效
        proxies={
            'https':'http://'+proxy,
            'http': 'http://'+proxy
        }
        params1={
            'ip':'',
            'type':'0'
        }
        https_url = 'https://ip.cn/api/index'
        http_url = 'http://ip111.cn/'
        headers = {'User-Agent': 'curl/7.29.0'}
        try:
            https_r = requests.get(https_url, headers=headers,params=params1, proxies=proxies, timeout=10)
            http_r = requests.get(http_url, headers=headers, proxies=proxies, timeout=10)
        except Exception as e:
            return False
        if http_r.status_code!=200 or https_r.status_code!=200:
            return False
        return True
    proxies=loadProxies()
    position=checkProxies(proxies)
    if position==[]:
        pass
    else:
        for x in position[::-1]:
            proxies=delProxy(proxies, x)
        proxies=addProxies(proxies, size)
    saveProxies(proxies)
    
def getProxy(localip=False):    #程序调用代理的接口
    def loopProxy(proxies):
        newproxy=[]
        for x in range(len(proxies)):
            newproxy.append(proxies[x-1])
        return newproxy
    if localip==False:
        proxies=loadProxies()
        proxies=loopProxy(proxies)
        saveProxies(proxies)
        pro={
                'https':'http://'+proxies[0][0],
                'http': 'http://'+proxies[0][0]
        }
    else:
        pro={}
    return pro

def getProxies(int=10):         #从网上采集ip
    def myIp():
        params1={
            'ip':'',
            'type':'0'
        }
        https_url = 'https://ip.cn/api/index'
        headers = {'User-Agent': 'curl/7.29.0'}
        try:
            https_r = requests.get(https_url, headers=headers,params=params1, timeout=10)
        except Exception as e:
            return ''
        httpst=https_r.json()
        if https_r.status_code!=200:
            return ''
        return httpst['ip']
    def addwhitename():
        ip=myIp()
        URL='https://wapi.http.linkudp.com/index/index/save_white?neek=397501&appkey=513e1865b62efeb560045e1e7d8f9900&white='+ip
        res=requests.get(URL)
        return (res.json()['code'])
    def deletewhitename():
        ip=myIp()
        URL='https://wapi.http.linkudp.com/index/index/del_white?neek=397501&appkey=513e1865b62efeb560045e1e7d8f9900&white='+ip
        res=requests.get(URL)
        return (res.json()['code'])
    proxyURL='http://webapi.http.zhimacangku.com/getip?type=2&pro=0&city=0&yys=0&port=1&time=1&ts=1&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions='
    addwhitename()
    res=requests.get(proxyURL+'&num='+str(int))
    if res.status_code!=200:
        print('[Proxy]:Proxy reject request:',res.status_code)
        return []
    rsts=res.json()['data']
    proxies=[[rst['ip']+':'+str(rst['port']),rst['expire_time']] for rst in rsts]
    deletewhitename()
    log.lognow.addValue('ipCount',int)
    return proxies

def saveProxies(proxies):   #将代理序列化并保存
    a=json.dumps(proxies)
    with proxylock:
        with open('proxies.json', 'w',encoding='utf-8') as f:
            f.write(a)

def loadProxies():          #将本地代理读取
    with proxylock:
        with open('proxies.json', 'r',encoding='utf-8') as f:
            proxies=json.loads(f.read())
    return proxies

if __name__=='__main__':
    invalidProxy({'https': 'http://183.56.105.7:4245', 'http': 'http://183.56.105.7:4245'})
    pass