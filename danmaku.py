import getHead
import requests
import output_file
import xml.etree.ElementTree as ET

cid=324408996
danmakuURL='http://comment.bilibili.com/'

def getDanmaku():
    head = {'user-agent': getHead.loadUa()}
    danmaku = requests.get(danmakuURL+str(cid)+'.xml',headers=head)
    return danmaku.content.decode()

def extractDanmaku(str):
    root = ET.fromstring(str)
    attr=[attrSave(x.attrib['p']+','+x.text) for x in root.iter('d')]
    print(attr)
    
    # for x in root.iter('d'):
    #     print(x.attrib['p'],x.text)
        # a+=1
        # if a>10:
        #     break

def attrSave(str):
    charcount=0
    # strcount=0
    lencount=0
    result=[]
    length=len(str)
    if length==0:
        return ['']
    for char in str:
        if char==',':
            result.append(str[:charcount])
            str=str[charcount+1:]
            charcount=0
            lencount+=1
            # strcount+=1
            continue
        lencount+=1
        charcount+=1
        if lencount>=length:
            result.append(str)
            break
    return result


if __name__=='__main__':
    # output_file.foutput(str(cid)+'danmaku.xml',getDanmaku())
    extractDanmaku(getDanmaku())
    # print(attrSave(',asda'))
