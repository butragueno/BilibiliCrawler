import getHead
import requests
import output_file
replyURL='http://api.bilibili.com/x/v2/reply'
aid=715178243


def getReply():
    params={'type':'1',
            'oid':str(aid),
    }
    head = {'user-agent': getHead.loadUa()}
    reply = requests.get(replyURL,params=params,headers=head)
    return reply.text



if __name__=='__main__':
    output_file.foutput(str(aid)+'reply.json',getReply())