'''Minehut server Api'''
from .config import *

serv_url = api_url + 'server/'

def getServerID(name: str) -> str:
    '''Return server ID by name'''
    url = serv_url + name + '?byName=true'
    res = req.get(url)
    # If request is good
    if res.ok:
        a = json.loads(res.text)['server']['_id']
    else:
        a = res
    return a

def getInfosbyName(name: str) -> json:
    '''Return server infos by name'''
    url = serv_url + name + '?byName=true'
    res = req.get(url)
    # If request is good
    if res.ok:
        a = json.loads(res.text)
    else:
        a = res
    return a


def getInfosbyID(id: str) -> json:
    '''Return server infos by ID'''
    url = serv_url + id
    res = req.get(url)
    # If request is good
    if res.ok:
        a = json.loads(res.text)
    else:
        a = res
    return a