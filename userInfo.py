import requests
import getHead
import math
import time

class user():
    def __init__(self,uid):
        self.mid=str(uid)
        
        self.infoURL='https://api.bilibili.com/x/space/acc/info?'
        self.statURL='https://api.bilibili.com/x/relation/stat?'
        self.videosURL="https://api.bilibili.com/x/space/arc/search"
        self.cardURL='http://api.bilibili.com/x/web-interface/card'

    def getInfo(self):
        params={
            'mid': self.mid,
            'jsonp': 'jsonp'
        }
        head = {'user-agent': getHead.loadUa(),
                'accept': 'application/json, text/plain, */*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-Language': 'zh-CN,zh;q=0.9',
                'origin': 'http://space.bilibili.com',
        }
        res = requests.get(self.infoURL,headers=head,params=params)
        info= res.json()
        try:
            infonew={
                "mid": info['data']['mid'],
                "name": info['data']['name'],
                "sex": info['data']['sex'],
                "sign": info['data']['sign'],
                "level": info['data']['level'],
                "silence": info['data']['silence'],
                "birthday": info['data']['birthday'],
                'viptype':info['data']['vip']['type'],
                'vipstatus':info['data']['vip']['status']
            }
        except:
            return {}
        return infonew

    def getStat(self):
        params={
            'vmid': self.mid,
            'jsonp': 'jsonp'
        }
        head = {'user-agent': getHead.loadUa(),
                'origin': 'http://space.bilibili.com',
        }
        res = requests.get(self.statURL,headers=head,params=params)
        stat= res.json()
        try:
            statnew={
                "follower":stat['data']['follower'],
                "following":stat['data']['following']
            }
        except:
            return {}
        return statnew

    def getVideoslist(self):
        params={
            'mid': self.mid,    #User's ID
            'ps': '30',         #Number of videos in each page
            'pn':'1',           #Page number
        }
        head = {'user-agent': getHead.loadUa(),
                'origin': 'http://space.bilibili.com',
        }
        res = requests.get(self.videosURL,headers=head,params=params)   #Get first page
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
            print('[Crawler][VideoList]',len(videosnew),'/',count,'records had been downloaded')
            if pagetotal==1:
                print('[Crawler][VideoList]',count-len(videosnew),'records had been dropped')
                return videosnew
            for x in range(2,pagetotal+1):
                params={
                'mid': self.mid,
                'ps': '30',
                'pn':str(x)
                }
                time.sleep(1)
                res = requests.get(self.videosURL,headers=head,params=params)
                videos= res.json()['data']['list']['vlist']
                for x in videos:
                    if x['mid']==int(self.mid): #Only count works of main user
                        videosnew.append([
                            x["aid"],
                            x["mid"],
                            x["bvid"]
                        ])
                print('[Crawler][VideoList]',len(videosnew),'/',count,'records had been downloaded')
            print('[Crawler][VideoList]',count-len(videosnew),'records had been dropped')
        except:
            print('[Crawler][VideoList]User:',self.mid,'has no videolist')
            return []
        return videosnew

    def getCard(self):
        params={
            'mid': self.mid,
        }
        head = {'user-agent': getHead.loadUa()
        }
        res = requests.get(self.cardURL,headers=head,params=params)
        card= res.json()
        time.sleep(1)
        try:
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
        except:
            cardnew=[]
            print('[Crawler][Card]User:',self.mid,'info is missing')
        return cardnew


if __name__=='__main__':
    starter(102, 150)
    pass
