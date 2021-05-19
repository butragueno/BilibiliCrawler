import requests
import getHead
import time

class video():
    def __init__(self,*vids):
        self.bvid=''
        self.aid=0
        self.detailURL='https://api.bilibili.com/x/web-interface/view/detail?'
        self.viewURL='http://api.bilibili.com/x/web-interface/view'
        self.tagsURL='http://api.bilibili.com/x/tag/archive/tags'
        if len(vids)>2 or len(vids)<1:
            raise AttributeError('Too much attributes')
        for vid in vids:
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

    def getDetail(self):
        params=self.params
        head = {'user-agent': getHead.loadUa(),
                'origin': 'http://www.bilibili.com',
        }
        res = requests.get(self.detailURL,headers=head,params=params)
        detail=res.json()['data']
        detailnew={
            "bvid": detail["View"]['bvid'],
            "aid": detail["View"]['aid'],
            "videos": detail["View"]['videos'],
            "partition":{
            "tid": detail["View"]['tid'],
            "tname": detail["View"]['tname']
            },
            "copyright": detail["View"]['copyright'],
            "title": detail["View"]['title'],
            "pubdate": detail["View"]['pubdate'],
            "desc": detail["View"]['desc'],
            "duration": detail["View"]['duration'],
            "owner": {
                "mid": detail["View"]['owner']['mid'],
                "name": detail["View"]['owner']['name']
            },
            "stat": {
                "aid": detail["View"]['stat']['aid'],
                "view": detail["View"]['stat']['view'],
                "danmaku": detail["View"]['stat']['danmaku'],
                "reply": detail["View"]['stat']['reply'],
                "favorite": detail["View"]['stat']['favorite'],
                "coin": detail["View"]['stat']['coin'],
                "share": detail["View"]['stat']['share'],
                "rank": detail["View"]['stat']['his_rank'],
                "like": detail["View"]['stat']['like']
            },
            "cid": detail['View']["cid"],
            "pages": [],
            'tags':[]
        }
        detailnew['pages']=[{
            "cid": x['cid'],
            "page": x['page'],
            "parttitle": x['part'],
            "duration": x['duration']
        } for x in detail['View']['pages']]
        detailnew['tags']=[{
            "tag_id": x["tag_id"],
            "tag_name": x["tag_name"]
        } for x in detail['Tags']]
        return detailnew

    def getView(self):
        params=self.params
        head = {'user-agent': getHead.loadUa(),
                'origin': 'http://www.bilibili.com',
        }
        res = requests.get(self.viewURL,headers=head,params=params)
        time.sleep(1)
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
            viewnew=[]
            print('[Crawler][View]Video:',viewnew[0],'info is missing')
        return viewnew

    def getpages(self):
        params=self.params
        head = {'user-agent': getHead.loadUa(),
                'origin': 'http://www.bilibili.com',
        }
        res = requests.get(self.viewURL,headers=head,params=params)
        time.sleep(1)
        try:
            pages=res.json()['data']
            pagesnew=[{
                'aid':pages['aid'],
                'bvid':pages['bvid'],
                "cid": x['cid'],
                "page": x['page'],
                "parttitle": x['part'],
                "duration": x['duration']
            } for x in pages['pages']]
            print('[Crawler]Video',[x for x in self.params.values()][0],'has',len(pagesnew),'pages')
        except:
            print('[Crawler]Video:',[x for x in self.params.values()][0],'has no pages info')
            return []
        return pagesnew

    def getTags(self):
        params=self.params
        head = {'user-agent': getHead.loadUa(),
                'origin': 'http://www.bilibili.com',
        }
        res = requests.get(self.tagsURL,headers=head,params=params)
        time.sleep(1)
        tagsaid=0
        tagsbvid=''
        try:
            tags=res.json()['data']
            if self.bvid=='':
                tagsaid=self.aid
            elif self.aid==0:
                tagsbvid=self.bvid
            else:
                tagsaid=self.aid
                tagsbvid=self.bvid
            tagsnew=[{
                'aid':tagsaid,
                'bvid':tagsbvid,
                "tag_id": x["tag_id"],
                "tag_name": x["tag_name"]
            } for x in tags]
            print('[Crawler]Video',[x for x in self.params.values()][0],'has',len(tagsnew),'tags')
        except:
            print('[Crawler]Video:',[x for x in self.params.values()][0],'has no tags info')
            return []
        return tagsnew

if __name__=='__main__':
    starter(0,20)