import random
def loadUa():
    uas = []
    with open("user_agents.txt", 'r') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[:-1])
    ua = random.choice(uas)
    return ua

if __name__=='__main__':
    pass