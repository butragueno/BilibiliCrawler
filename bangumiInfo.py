import getHead
import requests
import time
import math

def getIndex(page):
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
        'user-agent': getHead.loadUa(),
        'origin': 'https://www.bilibili.com',
    }
    res = requests.get(indexURL,headers=head,params=params)
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


class bangumi():
    def __init__(self,seasonId):
        self.seasonId=str(seasonId)
        self.seasonstatURL='https://api.bilibili.com/pgc/web/season/stat?'
        self.season2epURL='https://api.bilibili.com/pgc/web/season/section?'
        self.episodeURL='https://api.bilibili.com/pgc/season/episode/web/info?'
        self.detailURL='http://api.bilibili.com/pgc/view/web/season'

    def getSeasonStat(self):
        params={
            'season_id': self.seasonId,
        }
        head = {
            'user-agent': getHead.loadUa(),
            'origin': 'https://www.bilibili.com',
        }
        res = requests.get(self.seasonstatURL,headers=head,params=params)
        time.sleep(1)
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
            return []
        return ssstatnew

    def season2ep(self):
        params={
            'season_id': self.seasonId,
            }
        head = {
            'user-agent': getHead.loadUa(),
            'origin': 'https://www.bilibili.com',
        }
        res = requests.get(self.season2epURL,headers=head,params=params)
        return res.text

    def getEpisodestat(self,epid):
        params={
            'ep_id': str(epid),
        }
        head = {
            'user-agent': getHead.loadUa(),
            'origin': 'https://www.bilibili.com',
        }
        res = requests.get(self.episodeURL,headers=head,params=params)
        time.sleep(1)
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
            return []
        return epinfonew
    
    def getSeasoninfo(self):
        params={
            'season_id': self.seasonId
        }
        head = {
            'user-agent': getHead.loadUa()
        }
        res = requests.get(self.detailURL,headers=head,params=params)
        time.sleep(1)
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
        except:
            detailsnew=[]
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
        except:
            episodes=[]
        return detailsnew,episodes   

if __name__=='__main__':
    pass