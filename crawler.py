import getHead
import requests
import time
import math
import threading
from queue import Queue
import log
import proxyPool

def search(search_type,keyword,page=1): #用关键词搜索用户、视频、动画
    URL='https://api.bilibili.com/x/web-interface/search/type?'
    params={
        'search_type': search_type,
        'page':page,
        'keyword':keyword
    }
    res=connect(URL,params,True)
    try:
        results=res.json()['data']['result']
    except:
        return []
    if search_type=='video':
        result=[[
            x["title"],
            x["description"],
            x["author"],
            x["play"],
            x['video_review'],
            x["favorites"],
            x["review"],
            x["pubdate"],
            x["duration"],
            x["arcurl"]
        ] for x in results]
    elif search_type=='bili_user':
        result=[[
            x["uname"],
            x["mid"],
            x["usign"],
            x["fans"],
            x["videos"],
            x["level"],
            x["gender"],
            'https://space.bilibili.com/'+str(x["mid"])
        ] for x in results]
    if search_type=='media_bangumi':
        result=[[
            x["title"],
            x["areas"],
            x["desc"],
            x["pubtime"],
            x["media_score"]["user_count"],
            x["media_score"]["score"],
            x["goto_url"]
        ] for x in results]
    return result

def connect(URL,params,local=True): #将requests库的get函数和错误重试封装到一个函数中
    err=0
    while True:
        try:
            head = {
                'user-agent': getHead.loadUa()
            }
            proxies=proxyPool.getProxy(local)
            res = requests.get(URL,proxies=proxies,headers=head,params=params,timeout=10)
            time.sleep(1)
            break
        except Exception as e:
            print(e)
            print('Retrying...')
            proxyPool.invalidProxy(proxies)
            err+=1
        if err>=5:
            print('Retry failed')
            res=None
            break
    return res

def getIndex(page): #从动画索引页爬取动画ssid列表
    indexURL='https://api.bilibili.com/pgc/season/index/result'
    params={
        'season_version':'-1',
        'area':'-1',
        'is_finish':'-1',
        'copyright':'-1',
        'season_status':'-1',
        'season_month':'-1',
        'year':'-1',
        'style_id':'-1',
        'order':'3',
        'st':'1',
        'sort':'0',
        'page':str(page),
        'season_type':'1',
        'pagesize':'20',
        'type':'1'
    }
    head = {
        'user-agent': getHead.loadUa()
    }
    res = connect(indexURL,params=params)
    try:
        index=res.json()['data']['list']
        indexnew=[x["season_id"] for x in index]
        print('[Crawler][Index]Page:',page,',',page*20,'animes are downloaded')
        print('-----------------------------------------------------------------------')
    except:
        indexnew=[]
        print('[Crawler][Index]Page:',page,'are not downloaded')
        print('-----------------------------------------------------------------------')
    return indexnew

class bangumi(): #每个动画对应的ssid创建一个单独的类
    def __init__(self,seasonId):
        self.seasonId=str(seasonId)#ssid
        self.seasonstatURL='https://api.bilibili.com/pgc/web/season/stat?'
        self.season2epURL='https://api.bilibili.com/pgc/web/season/section?'
        self.episodeURL='https://api.bilibili.com/pgc/season/episode/web/info?'
        self.detailURL='http://api.bilibili.com/pgc/view/web/season'

    def getSeasonStat(self):    #获取动画对应的播放点赞收藏等状态数
        params={
            'season_id': self.seasonId,
        }
        head = {
            'user-agent': getHead.loadUa()
        }
        res = connect(self.seasonstatURL,params=params)
        try:
            ssstat=res.json()['result']
            ssstatnew=[
                ssstat['coins'],
                ssstat['danmakus'],
                ssstat['follow'],
                ssstat['likes'],
                ssstat['series_follow'],
                ssstat['views']
            ]
            print('[Crawler][SeasonStat]Season:',self.seasonId,'stat is downloaded')
        except:
            print('[Crawler][SeasonStat]Season:',self.seasonId,'stat is missing')
            return [None,None,None,None,None,None]
        return ssstatnew

    def getEpisodestat(self,epid):  #获取动画每集episode对应的状态数
        params={
            'ep_id': str(epid),
        }
        head = {
            'user-agent': getHead.loadUa(),
            'origin': 'https://www.bilibili.com',
        }
        res = connect(self.episodeURL,params=params)
        try:
            epinfo=res.json()['data']
            epinfonew=[
                epinfo['stat']['coin'],
                epinfo['stat']['dm'],
                epinfo['stat']['like'],
                epinfo['stat']['reply'],
                epinfo['stat']['view']
            ]
            print('[Crawler][EpisodeStat]Episode:',epid,'info is downloaded')
        except:
            print('[Crawler][EpisodeStat]Episode:',epid,'info is missing')
            return [None,None,None,None,None]
        return epinfonew
    
    def getSeasoninfo(self):    #获取动画的基本信息和分集列表
        params={
            'season_id': self.seasonId
        }
        head = {
            'user-agent': getHead.loadUa()
        }
        res = connect(self.detailURL,params=params)
        try:
            details=res.json()['result']
            detailsnew=[
                self.seasonId,
                details['evaluate'], 
                details['publish']['is_finish'],
                details['publish']['is_started'],
                details['publish']['pub_time'],
                details['publish']['unknow_pub_date'],
                details['rating']['count'],
                details['rating']['score'],
                details['season_title'],
                details['stat']['reply'],
                details['stat']['share'],
                details['total']
            ]
            print('[Crawler][SeasonInfo]Season:',self.seasonId,'info is downloaded')
            log.lognow.addValue('seasonCount')
        except:
            detailsnew=[self.seasonId,None,None,None,None,None,None,None,None,None,None,None]
            print('[Crawler][SeasonInfo]Season:',self.seasonId,'info is missing')
        try:
            episodes=[[
                x['id'],
                self.seasonId,
                x['aid'],
                x['bvid'],
                x['cid'],
                x['long_title'],
                x['pub_time'],
                x['title']
            ] for x in details['episodes']]
            print('[Crawler][EpisodeInfo]Season:',self.seasonId,'has',len(episodes),'episodes info')
            log.lognow.addValue('episodeCount',len(episodes))
        except:
            episodes=[]
        return detailsnew,episodes   

class user():   #每个用户对应的id创建一个单独的类
    def __init__(self,uid):
        self.mid=str(uid)
        self.infoURL='https://api.bilibili.com/x/space/acc/info?'
        self.statURL='https://api.bilibili.com/x/relation/stat?'
        self.videosURL="https://api.bilibili.com/x/space/arc/search"
        self.cardURL='http://api.bilibili.com/x/web-interface/card'

    def getVideoslist(self):    #每个用户所对应的视频列表
        def threadOn(pageQueue,listQueue):
            while not pageQueue.empty():
                try:
                    x=pageQueue.get(False)
                except:
                    break
                params={
                    'mid': self.mid,
                    'ps': '30',
                    'pn':str(x)
                }
                res = connect(self.videosURL,params=params)
                videos= res.json()['data']['list']['vlist']
                for video in videos:
                    if video['mid']==int(self.mid): #Only count works of main user
                        listQueue.put([
                            video["aid"],
                            video["mid"],
                            video["bvid"]
                        ])
                # print('Page:',x,'downloaded')
            i=b.wait()
            if i==0:
                event.set()
        params={
            'mid': self.mid,    #User's ID
            'ps': '30',         #Number of videos in each page
            'pn':'1',           #Page number
        }
        head = {'user-agent': getHead.loadUa(),
                'origin': 'http://space.bilibili.com',
        }
        res = connect(self.videosURL,params=params)   #Get first page
        try:
            videos= res.json()['data']['list']['vlist']
            count=0
            for x in res.json()['data']['list']['tlist'].values():
                count+=x['count']
            print('[Crawler][VideoList]User: ',self.mid,'has',count,'records')
            pagetotal=math.ceil(count/30)
            videosnew=[[
                x["aid"],
                x["mid"],
                x["bvid"]
            ] for x in videos if x['mid']==int(self.mid)]
            if pagetotal==1:
                print('[Crawler][VideoList]',len(videosnew),'/',count,'records had been downloaded')
                print('[Crawler][VideoList]',count-len(videosnew),'records had been dropped')
                return videosnew
            listQueue=Queue()
            pageQueue=Queue()
            ths=[]
            event=threading.Event()
            b=threading.Barrier(10)
            for x in range(2,pagetotal+1):
                pageQueue.put(x)
            for x in range(10):
                th=threading.Thread(target=threadOn,args=(pageQueue, listQueue))
                th.start()
            while not (event.isSet() and listQueue.empty()):
                try:
                    q=listQueue.get(False)
                except:
                    continue
                videosnew.append(q)
            print('[Crawler][VideoList]',len(videosnew),'/',count,'records had been downloaded')
            print('[Crawler][VideoList]',count-len(videosnew),'records had been dropped')
            log.lognow.addValue('videolistCount',len(videosnew))
        except:
            print('[Crawler][VideoList]User:',self.mid,'has no videolist')
            return []
        return videosnew

    def getCard(self):  #每个用户对应的基本信息
        params={
            'mid': self.mid,
        }
        head = {'user-agent': getHead.loadUa()
        }
        res = connect(self.cardURL,params=params)
        try:
            card= res.json()
            cardnew=[
                card['data']['card']['mid'],
                card['data']['card']['name'],
                card['data']['card']['sex'],
                card['data']['card']['sign'],
                card['data']['card']['level_info']['current_level'],
                card['data']['card']['birthday'],
                card['data']['card']['vip']['type'],
                card['data']['card']['vip']['status'],
                card['data']['card']['fans'],
                card['data']['card']['friend'],
                card['data']['archive_count']
            ]
            print('[Crawler][Card]User:',self.mid,'info is downloaded')
            log.lognow.addValue('userCount')
        except:
            cardnew=[self.mid,None,None,None,None,None,None,None,None,None,None]
            print('[Crawler][Card]User:',self.mid,'info is missing')
            log.lognow.addValue('userCount')
        return cardnew

class video():  #每个视频唯一对应的id创建实例
    def __init__(self,*vids):
        self.bvid=''
        self.aid=0
        self.detailURL='https://api.bilibili.com/x/web-interface/view/detail?'
        self.viewURL='http://api.bilibili.com/x/web-interface/view'
        self.tagsURL='http://api.bilibili.com/x/tag/archive/tags'
        if len(vids)>2 or len(vids)<1:
            raise AttributeError('Too much attributes')
        for vid in vids:    #判读输入的是aid还是bvid
            if isinstance(vid,str)==True:
                self.bvid=vid
            elif isinstance(vid,int)==True:
                self.aid=str(vid)
            elif isinstance(vid,(list,tuple))==True:
                for x in vid:
                    if isinstance(x,str)==True:
                        self.bvid=x
                    elif isinstance(x,int)==True:
                        self.aid=str(x)
                    else:
                        raise AttributeError('Wrong attribute',vid)
            else:
                raise AttributeError('Wrong attribute',vid)
        self.params={}  
        if self.bvid=='':
            self.params['aid']=self.aid
        elif self.aid==0:
            self.params['bvid']=self.bvid
        else:
            self.params['bvid']=self.bvid
            self.params['aid']=self.aid

    def getView(self):  #获取该视频的基本信息
        params=self.params
        head = {'user-agent': getHead.loadUa(),
                'origin': 'http://www.bilibili.com',
        }
        res = connect(self.viewURL,params=params)
        try:
            view=res.json()['data']
            viewnew=[
                view['aid'],
                view['bvid'],
                view['videos'],
                view['tid'],
                view['tname'],
                view['copyright'],
                view['title'],
                view['pubdate'],
                view['desc'],
                view['duration'],
                view['owner']['mid'],
                view['owner']['name'],
                view['stat']['view'],
                view['stat']['danmaku'],
                view['stat']['reply'],
                view['stat']['favorite'],
                view['stat']['coin'],
                view['stat']['share'],
                view['stat']['his_rank'],
                view['stat']['like'],
                view["cid"]
            ]
            print('[Crawler][View]Video:',viewnew[0],'info is downloaded')
        except:
            viewnew=[self.params['aid'],None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]
            print('[Crawler][View]Video:',self.params['aid'],'info is missing')
        log.lognow.addValue('videoCount')
        return viewnew

if __name__=='__main__':
    res=search('media_bangumi','黑')
    print(res)
    pass