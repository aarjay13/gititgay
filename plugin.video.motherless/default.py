#!/usr/bin/python
# -*- coding: utf-8 -*-
import xbmc, xbmcplugin, xbmcvfs, xbmcgui, xbmcaddon
import json as JSON
import sys
import urllib, urllib2
import time
import re
from htmlentitydefs import name2codepoint as n2cp
import httplib
import urlparse
from os import path, system
import socket
from urllib2 import Request, URLError, urlopen
from urlparse import parse_qs, urljoin, urlparse, urlunparse
from urllib import unquote_plus, basejoin, quote_plus
from motherlessvid import MotherlessVid
from xbmcUtils import xbmcUtils as xTools
thisPlugin = int(sys.argv[1])
Host = "http://motherless.com/"
VHost = "http://cdn.videos.motherlessmedia.com/videos/"
UrlGroupIdx = basejoin(Host, "groups/category")
UrlGroupVids = basejoin(Host, "gv/{0}/")
UrlSearch = basejoin(Host, "search/videos?term={0}&size=0&range=0&sort=date")
addonId = "plugin.video.motherless"
__addon__ = xbmcaddon.Addon(id=addonId)
#addonpath = path.join(path.abspath(__addon__.getSetting("path")), "resouces/")
xtool = xTools(addonid=addonId, pluginhandle=thisPlugin)
safeString = xtool.cleanStringMethod

addonpath = xtool.resDir
jsdecoder = JSON.JSONDecoder() #, object_hook=MotherlessVid)
jsdecoder.object_hook = MotherlessVid
jsdecoder.encoding = 'utf-8'
urljson = "http://motherless.com/feeds/groups/{0}/videos?format=json"
grouplist = ["twinks_and_boys", "mmmmm_boys", "brothers", "teen_boys_with_teen_boys", "boys4boys", "straight_men_having_fun_with_men", "masturbate_for_me___", "amateur_male_masturbation", "homoerotic_haven", "wank_world", "gay_daddies_and_older_brothers", "gay_incest", "_family_and_incest_stuff_", "boy_twink_ass", "debbie_hearts_favorite_twinks", "amateur_men_who_deserve_to_be_worshipped"]
starturls = ['http://motherless.com/groups/category/boys', 'http://motherless.com/groups/category/gay', 'http://motherless.com/groups/category/public', 'http://motherless.com/groups/category/webcams', 'http://motherless.com/groups/category/amateur', 'http://motherless.com/groups/category/masturbation', 'http://motherless.com/groups/category/incest', 'http://motherless.com/groups/category/pissing']
dataPath = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
if not path.exists(dataPath):
    xbmcvfs.mkdir(dataPath)
std_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.6) Gecko/20100627 Firefox/3.6.6',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-us,en;q=0.5',}

def getUrl(url):
    req = urllib2.Request(url)
    req.headers.update(std_headers)
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    return str(link)

def showContent():
    pic = path.join(addonpath, "search.png")
    addDirectoryItem("Search", {"name": "Search", "url": UrlSearch, "mode": 4}, pic)
    showGroups()
    groupsre = r'bio start.*?<a href="(.+)">.*?src="(http://cdn.images.motherlessmedia.com.+jpg)".*?bio end'
    regroup = re.compile(groupsre, re.DOTALL + re.M)
    for category in starturls:
        match = regroup.findall(getUrl(category))
        if match is not None:
            cmatch = str(match[:])
            cname = str(category).replace("http://motherless.com/groups/category/", "")
            catname = "[COLOR red]{0}[/COLOR] #[B]{1}[/B] Category".format(cname.title(), str(len(cmatch)))
            addDirectoryItem(catname, {"name": catname, "url": category, "mode": 1}, "DefaultVideoPlaylists.png")
    xtool.setView()


def getMenu(match):
    content = getUrl(Host)
    for gurl, thumb in match:
        fullurl = basejoin(Host, str(gurl).rpartition('/')[2])
        #vurl = str(basejoin(VHost,str(gurl).rpartition('/')[2]) + ".mp4")
        pic = thumb
        name = str(gurl)
        addDirectoryItem(name, {"name": fullurl, "url": gurl, "mode": 5}, pic)
    n1 = content.find('<div class="sub_menu dark-menu">', 0)
    n2 = content.find('<div class="inner-menu">', n1)
    content = content[n1:n2]
    i1 = 0
    if i1 == 0:
        regexcat = '<a href="(.*?)" title="(.*?)"'
        match = re.compile(regexcat, re.DOTALL).findall(content)
        for url, name in match:
            url1 = "http://motherless.com" + url
            pic = "DefaultVideoPlaylists.png"
            addDirectoryItem(name, {"name": name, "url": url1, "mode": 1}, pic)
    return xtool.setView()


def showGroups():
    listurls = []
    picfolder = path.join(xtool.resDir, "blackfolder.png")
    for group in grouplist:
        grp = str(group)
        grpurl = str(urljson.format(grp))
        listurls.append(grpurl)
        addDirectoryItem(grp, {"name": grp, "url": grpurl, "mode": 6}, picfolder)

def loadGroup(groupname, urljson):
    xbmcplugin.setPluginCategory(thisPlugin, "GROUP: {0}".format(groupname))
    strjson = getUrl(urljson)
    mvids = []
    jsdecoder.object_hook = MotherlessVid
    try:
        mvids = [jsdecoder.decode(strjson)]
    except:
        print "Couldn't decode JSON {0} {1}".format(groupname, urljson)
        ok = getVideos(groupname, UrlGroupVids.format(groupname))
    if len(mvids) > 0:
        for avid in mvids:
            try:
                vid = MotherlessVid(**avid)
                assert isinstance(vid, MotherlessVid)
                #vid.size.duration = vid.size._setDuration(seconds=vid.size.seconds)
                #vidurl = basejoin(Host, str(vid.link.rsplit('/',1)[0]))
                vidurl = str(basejoin(VHost, str(vid.link.rpartition('/')[2])) + ".mp4")
                xtool.addLink(videourl=vidurl, name=vid.label, iconImage=vid.thumbnail, plot=vid.label2, genre=groupname, duration=vid.size.duration, mode='5')
                #addDirectoryItem(vid.label, {"name": vid.title, "url": vid.url, "mode": 3}, vid.thumbnail, lbl2=vid.label2)
            except:
                print (str("FAILED IN ADDING VIDEO FROM JSON FOR LOOP {0}".format(str(vid.values()))))
        ok = xtool.setView()
    return ok

def getPage(name, url):
    pages = [1, 2, 3, 4, 5, 6]
    for page in pages:
        url1 = url + "?page=" + str(page)
        if str(url1).find("motherless.com") == -1:
            url1 = basejoin("http://motherless.com/", url1)
        name = "Page " + str(page)
        pic = "DefaultGenre.png"
        addDirectoryItem(name, {"name": name, "url": url1, "mode": 2}, pic)
    xtool.setView()


def getVideos(name1, urlmain):
    content = getUrl(urlmain)
    regexvideo = 'class="thumb video medium.*?<a href="(.*?)".*?img class="static" src="(.*?)".*?alt="(.*?)"'
    match = re.compile(regexvideo, re.DOTALL).findall(content)
    for url, pic, name in match:
        name = name.replace('"', '')
        url = str(url.replace(Host, '').rpartition('/')[2])
        vurl = str(basejoin(VHost, url) + ".mp4")
        purl = str(basejoin(Host, url))
        pic = pic
        #vidurl = basejoin(Host, str(url.rsplit('/',1)[0]))
        xtool.addLink(videourl=vurl, name=name, iconimage=pic, plot="{0} {1}".format(name, purl), genre="Porn", duration="", mode="5")
        #addDirectoryItem(name, {"name": name, "url": url, "mode": 3}, pic)
    xtool.setView()

def getSearch(name, url):    
    name1 = name.replace(" ", "+")
    #pages = [1, 2, 3, 4, 5, 6]
    for page in range(1, 10):
        purl = str(url + "&page={0}".format(str(page))) #"http://motherless.com/term/videos/" + name1 + "?range=0&size=0&sort=relevance&page=" + str(page)
        label = "{0} Search Result Page #{1}".format(name, str(page))
        pname = str("Page {0}".format(str(page)))
        pic = "DefaultVideos.png "
        #xtool.addLink(videourl=url, name=name, iconimage=pic, mode='5')
        addDirectoryItem(pname, {"name": pname, "url": purl, "mode": 2}, pic)
    return xtool.setView()

def playVideo(name, url):
    urlvid = str(basejoin(VHost,  str(url.rpartition('/')[2]) + ".mp4"))
    purl = str(basejoin(Host, str(url.rpartition('/')[2]) + ".mp4"))
    #if str(url).find("motherless.com") == -1:
    #    url = basejoin("http://motherless.com/", url.rpartition('/')[2])
    #fpage = str(getUrl(url))
    #match = re.compile("file.+'(http.+mp4).+'").findall(str(fpage)).pop()
    #match = re.compile(regexvideo, re.DOTALL).findall(fpage)
    #if match is not None:
    #    matchurl = str(match)
    #else:
    #    matchurl =
        #matchurl = str('http://' + fpage.split('.mp4', 1)[0].rpartition('http://')[2] + '.mp4') #index('fpage.find(".mp4"),
    #urlvid = matchurl
    pic = "DefaultVideo.png"
    li = xbmcgui.ListItem(label="{0} {1}".format(name, urlvid), label2=url, iconImage=pic, thumbnailImage=pic, path=purl)
    #liz = xtool.addLink(videourl=urlvid, name=name, iconimage=pic, plot=url, genre="Porn", mode='5', returnItem=True)
    assert isinstance(li, xbmcgui.ListItem)
    player = xbmc.Player(playerCore=xbmc.PLAYER_CORE_AUTO)
    li.setInfo('video', {'title': name})
    #xbmcplugin.addDirectoryItem(thisPlugin, urlvid, li, False, 1)
    #ok = xbmcplugin.endOfDirectory(thisPlugin, True, True, True)
    player.play(urlvid, li)
    return ok

def addDirectoryItem(name, parameters={}, pic="DefaultVideoCover.png", lbl2=""):
    li = xbmcgui.ListItem(label=name, label2=lbl2, iconImage=pic, thumbnailImage=pic)
    url = sys.argv[0] + '?' + urllib.urlencode(parameters)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=True)

def parameters_string_to_dict(parameters):
    ''' Convert parameters encoded in a URL to a dict. '''
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict

params = parameters_string_to_dict(sys.argv[2])
name = unquote_plus(str(params.get("name", ""))).replace('+', ' ')
url = urllib.unquote(str(params.get("url", "")))
mode = str(params.get("mode", ""))

if not sys.argv[2]:
    ok = showContent()
else:
    if mode == str(1):
        ok = getPage(name, url)
    elif mode == str(6):
        ok = loadGroup(groupname=name, urljson=url)
    elif mode == str(2):
        ok = getVideos(name, url)
    elif mode == str(5) or mode.lower().find('play') or mode == str(3):        
        ok = playVideo(name, url)
    elif mode == str(4):
        kb = xbmc.Keyboard(line='', heading='Search MOTHERLESS', hidden=False)
        kb.doModal()
        sname = None
        if kb.isConfirmed():
            sname = str(kb.getText())
        ok = getSearch(sname, UrlSearch.format(sname))


