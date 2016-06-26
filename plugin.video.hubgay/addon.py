# -*- coding: utf-8 -*-
from kodiswift import Plugin, xbmc, xbmcgui, xbmcaddon, xbmcplugin, xbmcvfs, xbmcmixin, ListItem
import json, sys, os, os.path as path, urllib, urllib2, re
from operator import itemgetter
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
APIURLS = {"gaytube": "http://www.gaytube.com/api/webmasters/search/?ordering=newest&period=alltime&thumbsize=all&count=100&page=1&tags[]=&search=", "pornhub": "http://www.pornhub.com/webmasters/search?id=44bc40f3bc04f65b7a35&search=&tags[]=gay&page=1&thumbsize=medium", "redtube": "http://api.redtube.com/?data=redtube.Videos.searchVideos&output=json&search=&tags[]=gay&page=1&thumbsize=medium", "spankwire": "http://www.spankwire.com/api/HubTrafficApiCall?data=searchVideos&output=json&search=&tags=gay&thumbsize=medium&page=1&segment=gay&count=100", "tube8": "http://api.tube8.com/api.php?action=searchVideos&output=json&search=gay&thumbsize=all&page=1&orientation=gay", "xtube": "http://www.xtube.com/webmaster/api.php?action=getVideosBySearchParams&tags=gay&count=100&thumbsize=400x300&fields=rating,username,title,tags,duration,thumbnail,url,embed,categories&page=1&search=", "youporn": "http://www.youporn.com/api/webmasters/search?search=&page=1&tags[]=gay&thumbsize=medium"}

def makeFolderItems(itemlist):
    litems = []
    for item in itemlist:
        assert isinstance(item, dict)
        litems.append(dict(path=item.get('path')))
    return litems

def makeItemExtraThumbs(item, vid):
    getsrc = itemgetter('src')
    xitem = plugin._listitemify(item=item)
    img = []
    thumbslist = vid.get('thumbs')
    if thumbslist.has_key('big'):
        img = thumbslist.get('big')
    else:
        for i in vid.get('thumbs'): img.append(getsrc(i))
    if len(img) > 0:
        artdict = {"thumb": img[0], "poster": img[1], "banner": img[2], "fanart": img[3], "clearart": img[4],
                   "clearlogo": img[5], "landscape": img[6], "fanart1": img[7], "fanart2": img[8], "fanart3": img[9]}
        xitem.set_art(artdict)
    return xitem

def makeVideoItems(itemlist, aslistitem=False):
    litems = []
    vitem = dict()
    vid = dict()
    item = dict()
    getsrc = itemgetter('src')
    try:
        for vitem in itemlist:
            assert isinstance(vitem, dict)
            if vitem.has_key('video'):
                vid = vitem.get('video')
            else:
                vid = vitem
            if vid is not None:
                assert isinstance(vid, dict)
                thumb = ''
                length = ''
                vidid = ''
                vurl = ''
                vtitle = ''
                pubdate = ''
                if vid.has_key('url'): vurl = vid.get('url')
                elif vid.has_key('embed'): vurl = vid.get('embed')
                if vid.has_key('default_thumb'): thumb = vid.get('default_thumb')
                elif vid.has_key('thumbnail'): thumb = vid.get('thumbnail')
                elif vid.has_key('thumb'): thumb = vid.get('thumb')
                if vid.has_key('duration'): length = vid.get('duration')
                if vid.has_key('id'): vidid = vid.get('id')
                elif vid.has_key('video_id'): vidid = vid.get('video_id')
                else: vidid = vurl.rsplit('-', 1)[0]
                if vid.has_key('title'): vtitle = vid.get('title').title()
                elif vitem.has_key('title'): vtitle = vitem.get('title').title()
                if vid.has_key('publish_date'): pubdate = vid.get('publish_date')
                elif vitem.has_key('publish_date'): pubdate = vitem.get('publish_date')
                vtitle = vtitle.replace('"', '')
                vtitle = vtitle.replace("'", '')
                lbl = vtitle
                lbl2 = "{0} {1}".format(pubdate, vidid)
                if length != "00:00:00" and length != '':
                    if length.find(':') == -1:
                        lenint = 0
                        seconds = int(length)
                        m, s = divmod(seconds, 60)
                        h, m = divmod(m, 60)
                        length = "%02d:%02d" % (m, s)
                        if h > 0: length = "%d:%02d:%02d" % (h, m, s)
                    else:
                        length = length.replace("00:","").lstrip("0")
                    lbl += '|[COLOR green]{0}[/COLOR]'.format(length)
                vpath = plugin.url_for(play, url=vurl, video=vidid)
                item = dict(label=lbl, label2=lbl2, icon=thumb, thumb=thumb, path=vpath, is_playable=True)
                item.setdefault(item.keys()[0])
                xbmc.log("Item {0} - {1} - {2} - {3}\n".format(vtitle, lbl2, thumb, vpath))
                if aslistitem:
                    litems.append(makeItemExtraThumbs(item, vid))
                else:
                    litems.append(item)
            else:
                xbmc.log("Item has no video key: {0}\n".format(repr(vitem)))
    except:
        xbmc.log("ERROR MAKINGVIDEOITEMS: {0}\n".format(repr(vitem)))
    allitems = sorted(litems, key=lambda litems: litems['label'])
    xbmc.log("\nFINISHED MakeVidItems: #{0} {1}\n".format(len(allitems), repr(allitems)))
    return allitems

def parseVideosUrl(url):
    obj = dict()
    if url.find('xtube.com') != -1: obj = []
    resp = ''
    resp = urllib2.urlopen(url).read()
    obj = json.loads(unicode(resp).decode('ascii'))
    if url.find('xtube.com') != -1: return obj
    try:
        if len(obj.keys()) == 1: return obj.get(obj.keys()[0])
        elif obj.has_key('videos'): return obj.get('videos')
        else: return obj
    except:
        return obj

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

def fullpathrootitems():
    pgay = plugin.url_for(site, sitename="gaytube", section="index", url="http://www.gaytube.com/api/webmasters/search/?ordering=mostviewed&period=alltime&thumbsize=all&count=100&tags[]=public,twink,webcam,bb,gay,bareback,amateur&search=")
    pph = plugin.url_for(site, sitename="pornhub", section="index", url="http://www.pornhub.com/webmasters/search?id=44bc40f3bc04f65b7a35&search=&tags[]=gay&thumbsize=medium")
    prt = plugin.url_for(site, sitename="redtube", section="index", url="http://api.redtube.com/?data=redtube.Videos.searchVideos&output=json&search=&tags[]=gay&thumbsize=medium")
    psw = plugin.url_for(site, sitename="spankwire", section="index", url="http://www.spankwire.com/api/HubTrafficApiCall?data=searchVideos&output=json&search=&tags=gay&thumbsize=medium&segment=gay&count=100")
    pt8 = plugin.url_for(site, sitename="tube8", section="index", url="http://api.tube8.com/api.php?action=searchVideos&output=json&search=gay&thumbsize=all&orientation=gay")
    pxt = plugin.url_for(site, sitename="xtube", section="index", url="http://www.xtube.com/webmaster/api.php?action=getVideosBySearchParams&search=gay")
    pyp = plugin.url_for(site, sitename="youporn", section="index", url="http://www.youporn.com/api/webmasters/search?search=&tags[]=gay&thumbsize=medium")

def rootItems():
    litems = []
    igay = __imgsearch__.replace('search.', 'fgaytube.')
    iph = __imgsearch__.replace('search.', 'fpornhub.')
    irt = __imgsearch__.replace('search.', 'fredtube.')
    isw = __imgsearch__.replace('search.', 'fspankwire.')
    it8 = __imgsearch__.replace('search.', 'ftube8.')
    ixt = __imgsearch__.replace('search.', 'fxtube.')
    iyp = __imgsearch__.replace('search.', 'fyouporn.')
    pgay = plugin.url_for(siteroot, sitename="gaytube")
    pph = plugin.url_for(siteroot, sitename="pornhub")
    prt = plugin.url_for(siteroot, sitename="redtube")
    psw = plugin.url_for(siteroot, sitename="spankwire")
    pt8 = plugin.url_for(siteroot, sitename="tube8")
    pxt = plugin.url_for(siteroot, sitename="xtube")
    pyp = plugin.url_for(siteroot, sitename="youporn")
    item = {'label': 'Gaytube', 'icon': igay, "thumb": igay, 'path': pgay}
    litems.append(item)
    item = {'label': 'Pornhub', 'icon': iph, "thumb": iph, 'path': pph}
    litems.append(item)
    item = {'label': 'Redtube', 'icon': irt, "thumb": irt, 'path': prt}
    litems.append(item)
    item = {'label': 'Spankwire', 'icon': isw, "thumb": isw, 'path': psw}
    litems.append(item)
    item = {'label': 'Tube8', 'icon': it8, "thumb": it8, 'path': pt8}
    litems.append(item)
    item = {'label': 'xtube', 'icon': ixt, "thumb": ixt, 'path': pxt}
    litems.append(item)
    item = {'label': 'YouPorn', 'icon': iyp, "thumb": iyp, 'path': pyp}
    litems.append(item)
    allitems = []
    for li in litems:
        li.setdefault(li.keys()[0])
        allitems.append(li)
    return sorted(allitems, key=lambda allitems: allitems['label'])

@plugin.route('/')
def index():
    itemlist = []
    allitems = []
    litems = []
    litems = rootItems()
    item = {'label': 'Search', 'path': plugin.url_for('search'), 'icon': __imgsearch__, 'thumb': __imgsearch__}
    item.setdefault(item.keys()[0])
    litems.append(item)
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

@plugin.route('/search/')
def search():
    searchtxt = ''
    searchtxt = plugin.get_setting('lastsearch')
    searchtxt = plugin.keyboard(searchtxt, 'Search Spankwire', False)
    searchquery = searchtxt.replace(' ', '+')
    plugin.set_setting(key='lastsearch', val=searchtxt)
    url = searchurl.format(searchquery)
    itemslist = parseVideosUrl(url)
    viditems = makeVideoItems(itemslist)
    return viditems

@plugin.route('/siteroot/<sitename>/')
def siteroot(sitename):
    siteurl = APIURLS.get(sitename)
    #plugin.redirect(plugin.url_for(site, sitename=sitename, section='index', url=siteurl))
    litems = site(sitename, 'index', siteurl)
    return litems


@plugin.route('/site/<sitename>/<section>/<url>/')
def site(sitename, section, url):
    litems = []
    itemslist = []
    siteurl = APIURLS.get(sitename)
    __imgnext__ = __imgsearch__.replace('search.png', 'next.png')
    if siteurl.find('search=gay') != -1:
        surl = siteurl.replace('search=gay&', 'search=gay+{0}&')
    else:
        surl = siteurl.replace('search=&', 'search={0}&')
    itemsearch = {'label': 'Search {0}'.format(sitename.title()),
            'path': plugin.url_for(site, sitename=sitename, section='search', url=surl), 'icon': __imgsearch__,
            'thumb': __imgsearch__}
    itemsearch.setdefault(itemsearch.keys()[0])
    pagenum = 2
    if url.find('page=') != -1:
        pagestr = str(url.split('page=',1)[1]).split('&',1)[0]
        if pagestr is not None: pagenum = int(pagestr)+1
    pagenumcur = pagenum - 1
    #tempu = url[url.find('page=')]
    if url.find('page=1') != -1:
        nurl = url.replace('page=1', 'page=2')
    elif url.find('page=') != -1:
        nurl = url.replace('page={0}'.format(pagenumcur), 'page={0}'.format(pagenum))
    else:
        nurl = url + '&page={0}'.format(pagenum)
    itemnext = {'label': 'Next --> {0}'.format(pagenum), 'path': plugin.url_for(site, sitename=sitename, section='next', url=nurl), 'icon': __imgnext__, 'thumb': __imgnext__}
    itemnext.setdefault(itemnext.keys()[0])
    if section.lower() == "index":
        vitems = list()
        itemslist = parseVideosUrl(url)
        litems = makeVideoItems(itemslist)
        try:
            itemslist = sorted(litems, key=lambda litems:litems['label'])
        except:
            xbmc.log('\nERROR SORTING ITEMS #{0}'.format(len(litems)))
            itemslist = litems
        itemslist.insert(0, itemsearch)
        itemslist.append(itemnext)
        litems = itemslist
    elif section.lower() == "next":
        vitems = list()
        itemslist = parseVideosUrl(url)
        litems = makeVideoItems(itemslist)
        try:
            itemslist = sorted(litems, key=lambda litems:litems['label'])
        except:
            xbmc.log('\nERROR SORTING ITEMS #{0}'.format(len(litems)))
            itemslist = litems
        itemslist.insert(0, itemsearch)
        itemslist.append(itemnext)
        litems = itemslist
    elif section.lower() == "search":
        searchtxt = ''
        searchtxt = plugin.get_setting('lastsearch')
        searchtxt = plugin.keyboard(searchtxt, 'Search {0}'.format(sitename.title()), False)
        searchquery = searchtxt.replace(' ', '+')
        plugin.set_setting(key='lastsearch', val=searchtxt)
        surl = surl.format(searchquery)
        xbmc.log('SEARCH - {0} - URL {1}'.format(searchquery, surl))
        itemslist = parseVideosUrl(surl)
        litems = makeVideoItems(itemslist)
        try:
            itemslist = sorted(litems, key=lambda litems:litems['label'])
        except:
            xbmc.log('\nERROR SORTING ITEMS #{0}'.format(len(litems)))
            itemslist = litems
        itemslist.insert(0, itemsearch)
        nurl = surl.replace('page=1', 'page=2')
        itemnext = {'label': 'Next {0} --> {1}'.format(searchtxt, pagenum),
                    'path': plugin.url_for(site, sitename=sitename, section='next', url=nurl), 'icon': __imgnext__,
                    'thumb': __imgnext__}
        itemnext.setdefault(itemnext.keys()[0])
        itemslist.append(itemnext)
        litems = itemslist
    else:
        itemslist = parseVideosUrl(url)
        litems = makeVideoItems(itemslist)
        litems.append(itemnext)
    return litems

@plugin.route('/category/<catname>/<url>/')
def category(catname, url):
    if url is None: url = caturl.format(catname)
    url = urllib.unquote_plus(url).replace(' ', '+')
    itemslist = parseVideosUrl(url)
    xbmc.log("Parsed Vids list {0} {1}".format(len(itemslist), repr(itemslist)))
    litems = makeVideoItems(itemslist)
    xbmc.log("List Items {0} {1}".format(len(litems), repr(litems)))
    return litems

@plugin.route('/play/<video>/<url>/')
def play(video, url):
    vidhtml = urllib2.urlopen(url).read()
    matches = \
    re.compile('href="(http://cdn...download.spankwire.+mp4.+[^"])".', re.I + re.M + re.S + re.U).findall(vidhtml)[0]
    if matches is None:
        matches = re.compile("videoUrl: '([^']*)',", re.I + re.M + re.S + re.U).findall(vidhtml)[0]
        vidurl = matches
    else:
        vidurl = matches.split(' ', 1)[0].strip('"')
    xbmc.log("PLAY matches vidpage: \n{0}".format(vidurl))
    vli = ListItem(label=video, label2=url, icon="DefaultVideo.png", thumbnail="DefaultVideo.png", path=vidurl)
    vli.playable = True
    plugin.set_resolved_url(vli)
    plugin.play_video(vli)
    #xbmc.Player().play(vidurl, vli.as_xbmc_listitem())
    #return plugin.set_resolved_url(vli)
    #vidurl = "http://cdn2b.public.spankwire.phncdn.com/novideo.flv?ir=1953&rs=2000&s=1466541100&e=1466569900&h=7b4efeb5378339681485187a1755b859"
    #vidurl = "http://cdn2b.download.spankwire.phncdn.com/201606/20/5174721/mp4_high_5174721.mp4?ir=1953&rs=2000&s=1466541100&e=1466569900&h=d6cf4fe17926353e9b03150bee167908"


if __name__ == '__main__':
    plugin.run()
    viewmode = int(plugin.get_setting('viewmode'))
    if viewmode is None: viewmode = 500
    plugin.set_view_mode(viewmode)
    #xbmc.executebuiltin("Container.SetViewMode({0})".format(viewMode))
