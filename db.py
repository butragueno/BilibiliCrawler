import crawler
import sqlite3
import threading
import log
dblock=threading.Lock()
def initial(dbname): #初始化数据库
    conn = sqlite3.connect(dbname)
    # print('[Database]Open databass successfully')
    cur = conn.cursor()
    # print('[Database]Creat cursor successfully')
    return conn,cur

def creatTable(conn,cur):   #创建表
    #Create table users
    cur.execute('''CREATE TABLE if not exists users
    (
        mid          INT    PRIMARY KEY     NOT NULL,
        name         TEXT,
        sex          TEXT,
        sign         TEXT,
        level        INT,
        birthday     TEXT,
        viptype      INT,
        vipstatus    INT,
        follower     INT,
        following    INT,
        archiveCount INT
        );''')
    conn.commit()
    print('[Database][CreateTable]Create table USERS successfully')
    #Create table videolist
    cur.execute('''CREATE TABLE if not exists videolist
    (
        aid     INT     PRIMARY KEY     NOT NULL,
        mid     INT                     NOT NULL,
        bvid    TEXT                    NOT NULL
        );''')
    conn.commit()
    print('[Database][CreateTable]Create table VIDEOLIST successfully')
    cur.execute('''CREATE TABLE if not exists video
    (
        aid         INT     PRIMARY KEY NOT NULL,
        bvid        TEXT,
        videos      INT,
        tid         INT,
        tname       TEXT,
        copyright   INT,
        title       TEXT,
        pubdate     INT,
        desc        TEXT,
        duration    INT,
        mid         INT,
        name        TEXT,
        view        INT,
        danmaku     INT,
        reply       INT,
        favorite    INT,
        coin        INT, 
        share       INT, 
        rank        INT, 
        like        INT, 
        cid         INT
        );''')
    conn.commit()
    print('[Database][CreateTable]Create table VIDEO successfully')
    cur.execute('''CREATE TABLE if not exists episodes
    (
        episodeid   INT     PRIMARY KEY     NOT NULL,        
        seasonid    INT                     NOT NULL,
        aid         INT,
        bvid        TEXT,
        cid         INT,
        longtitle   TEXT,
        pubtime     INT,
        title       TEXT,
        coin        INT,
        danmaku     INT,
        like        INT,
        reply       INT,
        view        INT
        );''')
    conn.commit()
    print('[Database][CreateTable]Create table EPISODES successfully')
    cur.execute('''CREATE TABLE if not exists season
    (
        seasonid        int     primary key     not null,
        description     text,
        isfinish        int,
        isstarted       int,
        pubtime         text,
        unknowpubdate   int,
        ratingcount     int,
        score           int,
        title           text,
        replys          int,
        shares          int,
        total           int,
        coins           int,
        danmakus        int,
        follow          int,
        likes           int,
        seriesfollow    int,
        views           int
        );''')
    conn.commit()
    print('[Database][CreateTable]Create table SEASON successfully')
    print('[Database][CreateTable]Create Table Finished')
    print('-----------------------------------------------------------------------')

def userGo(conn,cur,card):  #储存user信息
    # print('[Database][User]Insert the datas into Database is starting....')
    if card==[]:
        print('[Database][User]No info')
        return False
    # Insert the datas
    # try:
    with dblock:
        cur.execute("INSERT OR IGNORE INTO users VALUES (?,?,?,?,?,?,?,?,?,?,?);",card)
        conn.commit()
    # except:
    #     conn.rollback()
    print('[Database][User]UID:',card[0],'info finished\n')
    log.lognow.addValue('userdataCount')
    return True

def videolistGo(conn,cur,videolist):    #储存videolist信息
    if videolist==[]:
        print('[Database][VideoList]User has no videolist')
        return False
    # Insert the datas
    # print('[Database][VideoList]Save the datas into Database is starting....')
    count=0
    for video in videolist:
        # try:
        with dblock:
            cur.execute("INSERT OR IGNORE INTO videolist VALUES (?,?,?)",video)
            conn.commit()
        count+=1    
        # except:
        #     conn.rollback()
        # if count%10==0:
        #     print('[Database][VideoList]Insert',count,'/',len(videolist),'records successfully')
    print('[Database][VideoList]User',count,'/',len(videolist),'records successfully\n')
    log.lognow.addValue('videolistdataCount')
    return True

def viewGo(conn,cur,view):  #储存video信息
    # print('[Database][View]Insert the datas into Database is starting....')
    if view==[]:
        print('[Database][View]Video: has no info')
        return False
    # Insert the datas
    with dblock:
        cur.execute("INSERT OR IGNORE INTO video VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);",view)
        conn.commit()
    print('[Database][View]Video:',view[0],'info had been finished')
    log.lognow.addValue('videodataCount')
    return True

def epGo(conn,cur,eps,epstats): #储存分集信息
    if eps==[]:
        print('[Database][Episode]Season has no episode')
        return False
    elif epstats==[]:
        print('[Database][Episode]Episode:',eps[0][0],'has no episode stat')
        epstats=[[
            0,
            0,
            0,
            0,
            0
        ]]*len(eps)
    # Insert the datas
    # print('[Database][Episode]Save the datas into Database is starting....')
    for x in range(len(eps)):
        with dblock:
            cur.execute("INSERT OR IGNORE INTO episodes VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",eps[x]+epstats[x])
            conn.commit()
        print('[Database][Episode]Episode:',eps[x][0],'info is finished')
    print('[Database][Episode]END: Insert',len(eps),'records successfully')
    log.lognow.addValue('episodedataCount',len(eps))
    return True

def seasonGo(conn,cur,ssstat,ssinfo):   #储存动画信息
    print('[Database][Season]Insert the datas into Database is starting....')
    if ssinfo==[]:
        print('[Database][Season]has no info')
        return False
    elif ssstat==[]:
        print('[Database][Season]',ssinfo[0],'has no stat')
        ssstat=[
            0,
            0,
            0,
            0,
            0,
            0
        ]
    # Insert the datas
    with dblock:
        cur.execute("INSERT OR IGNORE INTO season VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);",ssinfo+ssstat)
        conn.commit()
    log.lognow.addValue('seasondataCount')
    return True

if __name__=='__main__':
    pass