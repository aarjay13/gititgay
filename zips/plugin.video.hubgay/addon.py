# -*- coding: utf-8 -*-
from kodiswift import Plugin, xbmc, xbmcgui, xbmcaddon, xbmcplugin, xbmcvfs, xbmcmixin
import json, sys, os, os.path as path, urllib, urllib2

plugin = Plugin()
__addondir__ = xbmc.translatePath(plugin.addon.getAddonInfo('path'))
if __addondir__.startswith('/var'): __addondir__ = '/Users/jezza/PycharmProjects/repo-gaymods/plugin.video.hubgay/'
__resdir__ = path.join(__addondir__, 'resources')
__imgsearch__ = path.join(__resdir__, 'search.png')
urlbase = "http://www.spankwire.com/api/HubTrafficApiCall?"
caturl = urlbase + "data=getCategoriesList&output=json&segment=gay"
catvidsurl = urlbase + "data=searchVideos&output=json&thumbsize=small&count=100&segment=gay&search=&tags=&category={0}"
searchurl = urlbase + "data=searchVideos&output=json&thumbsize=small&count=100&segment=gay&search={0}&tags=&category="
thumbcaturl = "http://cdn2.static.spankwire.com/images/category/Gay/{0}.jpg"

def makeFolderItems(itemlist):
    litems = []
    for item in itemlist:
        assert isinstance(item, dict)
        litems.append(dict(path=item.get('path')))
    return litems

def makeVideoItems(itemlist):
    litems = []
    try:
        for vid in itemlist:
            assert isinstance(vid, dict)
            item = dict(path=plugin.url_for(play, url=vid.get('url'), video=item), label=vid.get('title'), icon=vid.get('default_thumb'), thumb=vid.get('thumb'), label2=vid.get('duration'), is_playable=True)
            vidpath = plugin.url_for(play, video=item, url=vid.get('url'))
            item.update(path=vidpath)
            item.setdefault(item.keys()[0])
            litems.append(item)
    except:
        return []
    return litems

def parseVideosUrl(url):
    resp = urllib2.urlopen(url).read()
    obj = json.loads(resp)
    if len(obj.keys) == 1: return obj.get(obj.keys[0])
    else: return obj

def readjson():
    dictallcats = dict()
    try:
        txt = file(path.join(__addondir__, 'spankwire.json'), 'r').read()
        dictallcats = json.loads(txt) #dictallcats = json.JSONDecoder().decode(txt)
        if len(dictallcats.keys) == 1: return dictallcats.get(dictallcats.get(dictallcats.keys[0]))
        else: return dictallcats
    except:
        return []

def savejson(obj, filename):
    try:
        f = file(filename, 'w')
        txt = json.dump(obj,f)
        f.close()
    except:
        pass

def make_catitems(dictallcats):
    listofcats = dictallcats.get(dictallcats.keys()[0])
    catvidslistitems = []
    for cat in listofcats:
        catname = cat.get('category')
        caturl = catvidsurl.format(catname)
        thumb = thumbcaturl.format(catname.replace(' ', '').replace('/', '').replace('&', ''))
        viditem = dict(label=catname, icon=thumb, thumb=thumb, path=plugin.url_for(category, catname=catname, url=caturl))
        viditem.setdefault(viditem.keys()[0])
        catvidslistitems.append(viditem)
    return catvidslistitems

@plugin.route('/')
def index():
    itemlist = []
    allitems = []
    litems = []
    item = {'label': 'Search', 'path': plugin.url_for('search'), 'icon': __imgsearch__, 'thumb': __imgsearch__}
    item.setdefault(item.keys()[0])
    litems = [item]
    txt = file(path.join(__addondir__, 'spankwire.json')).read()
    allitems = json.loads(txt)
    itemlist = allitems.get(allitems.keys()[0])
    allitems = sorted(itemlist, key=lambda itemlist: itemlist['label'])
    for li in allitems:
        assert isinstance(li, dict)
        catpath = plugin.url_for(category, catname=li.get('label'), url=li.get('path'))
        li.update(path=catpath)
        li.setdefault(li.keys()[0])
        litems.append(li)
    return litems

@plugin.route('/search')
def search():
    searchtxt = ''
    searchtxt = plugin.get_setting('lastsearch')
    searchtxt = plugin.keyboard(searchtxt, 'Search Spankwire', False)
    searchquery = searchtxt.replace(' ', '+')
    plugin.set_setting('lastsearch', searchtxt)
    url = searchurl.format(searchquery)
    itemslist = parseVideosUrl(url)
    viditems = makeVideoItems(itemslist)
    return viditems

@plugin.route('/category/<catname>/<url>')
def category(catname, url):
    if url is None: url = caturl.format(catname)
    itemslist = parseVideosUrl(url)
    return makeVideoItems(itemslist)

@plugin.route('/play/<video>/<url>')
def play(video, url):
    plugin.play_video(video)

if __name__ == '__main__':
    plugin.run()
