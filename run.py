import crawler
import math
import db
import proxyPool
import threading
import time
import log
from queue import Queue
def runTime(func):
    def wrapper(*args, **kw):
        start = time.time()
        func(*args, **kw)
        end = time.time()
        log.lognow.addValue('time',end-start)
        print('running', end-start, 's')
    return wrapper


@runTime
def userVideoThreadRun(STARTID=1,STOPID=1,para1=1,para2=3):
    def queueUid(uidQueue,STARTID,STOPID):
        for x in range(STARTID,STOPID+1):
            uidQueue.put(x)
        event1.set()
    def uidRun(uidQueue,videoQueue):
        while not (event1.isSet() and uidQueue.empty()):
            try:
                uid=uidQueue.get(False)
            except:
                break
            user=crawler.user(uid)
            card=user.getCard()
            videolist=user.getVideoslist()
            conn,cur=db.initial('bilibili.db')
            db.userGo(conn,cur,card)
            for video in videolist:
                videoQueue.put(video[0])
            db.videolistGo(conn,cur,videolist)
            conn.close()
        i1=b1.wait()
        if i1==0:
            print('what')
            event2.set()
    def videoRun(videoQueue):
        while not (event2.isSet() and videoQueue.empty()):
            try:
                vi=videoQueue.get()
            except:
                continue
            v=crawler.video(vi)
            view=v.getView()
            conn,cur=db.initial('bilibili.db')
            db.viewGo(conn, cur, view)
            conn.close()
    uidQueue=Queue()
    videoQueue=Queue()
    event1=threading.Event()
    event2=threading.Event()
    b1=threading.Barrier(para1)
    qu = threading.Thread(target=queueUid,args=(uidQueue,STARTID,STOPID))
    qu.daemon=True
    qu.start()
    urs = []
    for _ in range(para1):
        ur = threading.Thread(target=uidRun,args=(uidQueue,videoQueue))
        ur.daemon=True
        ur.start()
        urs.append(ur)
    vrs=[]
    for _ in range(para2):
        vr = threading.Thread(target=videoRun,args=(videoQueue,))
        vr.daemon=True
        vr.start()
        vrs.append(vr)
    qu.join()
    for ur in urs:
        ur.join()
    for vr in vrs:
        vr.join()
    print('-----------------------------------------------------------------------')
    # print('[RUN]The Database is closed') 
    print('[RUN]The Program is closed') 

@runTime
def userVideoRun(STARTID=1,STOPID=1):
    for uid in range(STARTID,STOPID+1):
        user=crawler.user(uid)
        card=user.getCard()
        videolist=user.getVideoslist()
        conn,cur=db.initial('bilibili.db')
        db.userGo(conn,cur,card)
        db.videolistGo(conn,cur,videolist)
        for video in videolist:
            vi=video[0]
            v=crawler.video(vi)
            view=v.getView()
            db.viewGo(conn, cur, view)
        conn.close()
        print('-----------------------------------------------------------------------')
    # print('[RUN]The Database is closed') 
    print('[RUN]The Program is closed') 


def bangumiRun(pagenow=1):
    TOTALbangumi=3335
    PAGESIZE=20
    TOTALPAGE=math.ceil(TOTALbangumi/PAGESIZE)
    conn,cur=db.initial('bilibili.db')
    # db.creatTable(conn, cur)
    for page in range(pagenow,2):
        indexs=crawler.getIndex(page)
        # indexs=range(36174,36175)
        for ssid in indexs:
            bang=crawler.bangumi(ssid)
            ssstat=bang.getSeasonStat()
            ssinfo,eps=bang.getSeasoninfo()
            epstats=[bang.getEpisodestat(x[0]) for x in eps]
            print('[Crawler][EpisodeStat]Season:',ssid,len(epstats),'episodes is downloaded\n')    
            db.seasonGo(conn,cur,ssstat,ssinfo)
            db.epGo(conn,cur,eps,epstats)
            print('[Starter]season:',ssinfo[-4],'are finished\n')
        print('[Starter]Bangumi Index:',page*20,'are finished')
        print('-----------------------------------------------------------------------')
    conn.close()
    print('[Run]Bangumi Index:',TOTALbangumi,'are finished')
    print('[RUN]The Program is closed') 

@runTime
def bangumiThreadRun(pagenow=1,pageend=1,para1=1,para2=5,para3=5):
    def indexRun():
        while not indexQueue.empty():
            try:
                page=indexQueue.get(False)
            except:
                continue
            indexs=crawler.getIndex(page)
            # indexs=range(36174,36175)
            for ssid in indexs:
                ssidQueue.put(ssid)
        i1=b1.wait()
        if i1==0:
            ev1.set()
    def ssidRun(para3):
        def epRun():
            while not (epidQueue.empty()):
                try:
                    epid=epidQueue.get(False)
                except:
                    continue
                stat=bang.getEpisodestat(epid)
                with eplock:
                    position=epstats.index(epid)
                    epstats[position]=stat
            i3=b3.wait()
            if i3==0:
                ev3.set()          
        while not (ev1.isSet() and ssidQueue.empty()):
            try:
                ssid=ssidQueue.get(False)
            except:
                continue
            bang=crawler.bangumi(ssid)
            ssstat=bang.getSeasonStat()
            ssinfo,eps=bang.getSeasoninfo()
            epidQueue=Queue()
            ev3=threading.Event()
            eplock=threading.Lock()
            b3=threading.Barrier(para2)
            epstats=[]
            for x in eps:
                epidQueue.put(x[0])
                epstats.append(x[0])
            sqs = []
            for _ in range(para3):
                sq = threading.Thread(target=epRun)
                sq.daemon=True
                sq.start()
                sqs.append(sq)
            for sq in sqs:
                sq.join()
            # print('[Crawler][EpisodeStat]Season:',ssid,len(epstats),'episodes is downloaded\n')  
            
            conn,cur=db.initial('bilibili.db')
            db.seasonGo(conn,cur,ssstat,ssinfo)
            db.epGo(conn,cur,eps,epstats)
            conn.close()
            # print('[Starter]season:',ssinfo[-4],'are finished\n')
    TOTALbangumi=3335
    PAGESIZE=20
    TOTALPAGE=math.ceil(TOTALbangumi/PAGESIZE)
    indexQueue=Queue()
    ssidQueue=Queue()
    ev1=threading.Event()
    b1=threading.Barrier(para1)
    for page in range(pagenow,pageend+1):
        indexQueue.put(page)
    irs=[]
    for _ in range(para1):
        ir=threading.Thread(target=indexRun)
        ir.daemon=True
        ir.start()
        irs.append(ir)
    srs = []
    for _ in range(para2):
        sr = threading.Thread(target=ssidRun,args=(para3,))
        sr.daemon=True
        sr.start()
        srs.append(sr)
    for ir in irs:
        ir.join()
    for sr in srs:
        sr.join()
    print('-----------------------------------------------------------------------')
    print('[Run]Bangumi Index:',TOTALbangumi,'are finished')
    print('[RUN]The Program is closed') 

def logger(i):
    if i==1:
        print('In this process, we have:')
        print('Used IP:              {}'.format(log.lognow.getValue('ipCount')))
        print('Downloaded user:      {}'.format(log.lognow.getValue('userCount')))
        print('Downloaded videolist: {}'.format(log.lognow.getValue('videolistCount')) )
        print('Downloaded video:     {}'.format(log.lognow.getValue('videoCount')))
        print('Saved user in DB:     {}'.format(log.lognow.getValue('userdataCount')))
        print('Saved videolist in DB:{}'.format(log.lognow.getValue('videolistdataCount')))
        print('Saved video in DB:    {}'.format(log.lognow.getValue('videodataCount')))
        log.lognow.saveValues()
    elif i==2:
        print('In this process, we have:')
        print('Used IP:              {}'.format(log.lognow.getValue('ipCount')))
        print('Downloaded season:    {}'.format(log.lognow.getValue('seasonCount')))
        print('Downloaded episode:   {}'.format(log.lognow.getValue('episodeCount')) )
        print('Saved season in DB:   {}'.format(log.lognow.getValue('seasondataCount')))
        print('Saved episode in DB:  {}'.format(log.lognow.getValue('episodedataCount')))
        log.lognow.saveValues()
    else:
        pass
def uv(start,stop):
    # proxyPool.createProxiesPool(20)
    userVideoThreadRun(start,stop,8,25)
    logger(1)
def ba(start,stop):
    proxyPool.createProxiesPool(20)
    bangumiThreadRun(start,stop,2,5,5)
    logger(2)

if __name__=='__main__':
    # proxyPool.saveProxies(proxyPool.getProxies(4))
    proxyPool.createProxiesPool(20)
    # userVideoThreadRun(1001,10000,8,25)
    bangumiThreadRun(5,2,5,5)
    logger(2)
    pass
