import os, sys, os.path as path
import json
import urllib, urllib2
import xbmcaddon
import xbmcgui
import xbmcplugin, xbmc, xbmcvfs
from xbmcUtils import xbmcUtils

thisPlugin = int(sys.argv[1])
addonId = "plugin.video.gayhub"
__addon__ = xbmcaddon.Addon(id=addonId)
xtool = xbmcUtils(addonid=addonId, pluginhandle=thisPlugin)
dictallcats = dict()
thumbcaturl = "http://cdn2.static.spankwire.com/images/category/Gay/{0}.jpg"
caturl = "http://www.spankwire.com/api/HubTrafficApiCall?data=getCategoriesList&output=json&segment=gay"
catvidsurl = "http://www.spankwire.com/api/HubTrafficApiCall?data=searchVideos&output=json&thumbsize=small&count=100&segment=gay&search=&tags=&category={0}"
searchurl = "http://www.spankwire.com/api/HubTrafficApiCall?data=searchVideos&output=json&thumbsize=small&count=100&segment=gay&search={0}&tags=&category="

url=None
name=None
thumb=None
mode=None


def readjson():
    try:
        f = file('spankwire.json', 'r')
        txt = f.read()
        f.close()
        dictallcats = json.JSONDecoder().decode(txt)
        clist = dictallcats.get('spankwire')
        return dictallcats
    except:
        dictallcats = {}
    return dictallcats

def url_for_category(catname='', sitename=''):
    sitedict = dictallcats.get(sitename)
    for entry in sitedict:
        if entry.get('label') == catname:
            return entry.get('path')

def addDirectoryItem(name, parameters={}, pic="DefaultFolder.png", lbl2=""):
    if lbl2 == "": lbl2 = name
    li = xbmcgui.ListItem(label=name, label2=lbl2, iconImage=pic, thumbnailImage=pic)
    url = sys.argv[0] + '?' + urllib.urlencode(parameters)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=True)

def make_viditems(itemlist):
    litems = []
    for item in itemlist:
        assert isinstance(item, dict)
        plugpath = item.get('path')
        name = item.get('label')
        if name == 'Bi': name = 'Bi/Straight Guys'
        elif name == 'Bears': name = 'Bears/Hairy'
        elif name == 'Solo': name = 'Solo & Masturbation'
        thumb = thumbcaturl.format(name.replace(' ', '').replace('/', '').replace('&', ''))
        sitename = plugpath.replace('http://', '').partition('/')[0].replace('www.', '').replace('.com', '').upper()
        litems.append(addDirectoryItem(name, parameters=dict(url=plugpath, mode=1, name="Category {0}".format(name)), pic=thumb, lbl2=sitename))
    return litems
    #return xtool.setView()

def make_catitems(dictallcats):
    listofcats = dictallcats.get('spankwire')
    catvidslistitems = []
    for cat in listofcats:
        catname = cat.get('category')
        caturl = catvidsurl.format(catname)
        thumb = thumbcaturl.format(catname.replace(' ', '').replace('/', '').replace('&', ''))
        viditem = dict(label=catname, iconImage=thumb, thumbnailImage=thumb, path=caturl)
        catvidslistitems.append(viditem)
    return catvidslistitems

def showContent():
    pic = path.join(xbmc.translatePath(__addon__.getAddonInfo('path')),'resources', 'search.png')
    params = {"mode": 10, "url": searchurl, "name": "Search"}
    addDirectoryItem(name="Search", parameters=params, pic=pic, lbl2="Spankwire Search")
    pic = path.join(xbmc.translatePath(__addon__.getAddonInfo('path')),'resources', 'blackfolder.png')
    params = {"mode": 1, "url": "http://www.spankwire.com/api/HubTrafficApiCall?data=searchVideos&output=json&thumbsize=small&count=200&segment=gay&search=&tags=&category=", "name": "All"}
    addDirectoryItem(name="Spankwire", parameters=params, pic=pic, lbl2="All Gay Spankwire")    
    #u = sys.argv[0] + "?" + urllib.urlencode({"mode": 10, "url": searchurl, "name": "Search"})
    #li = xbmcgui.ListItem(label="Search", iconImage=pic, path=u)
    #xtool.addListItem(liz=li, pathurl=u)
    #u = sys.argv[0] + "?" + urllib.urlencode({"mode": 1, "url": "http://www.spankwire.com/api/HubTrafficApiCall?data=searchVideos&output=json&thumbsize=small&count=200&segment=gay&search=&tags=&category=", "name": "All"})
    #li = xbmcgui.ListItem(label="Spankwire", iconImage=pic, path=u)
    #xtool.addListItem(liz=li, pathurl=u)    
    #return xtool.setView()

def GetVideos(name, url):
    print "Get videos {0} {1}".format(name, url)
    try:
      content = urllib2.urlopen(url).read()
      rawjson = json.loads(content.decode('utf-8'))
      #print "Get videos content = " + content + " json = " + repr(rawjson)
      #xbmc.log("Get videos content = " + content + " json = " + repr(rawjson))
      #dictresults = rawjson.get('videos') # 
      dictresults = json.JSONDecoder().decode(rawjson)
      listvids = []
      listvids = dictresults.get('videos')
      for vid in listvids:
        assert isinstance(vid, dict)
        item = dict()
        item = vid.get('video')
        xtool.addLink(videourl=item.get('url'), name=item.get('title'), iconimage=item.get('default_thumb'), fanart=item.get('thumb'), duration=item.get('duration'), mode=2)      
      xtool.log(content)
    except:
      print "Error getting videos"
    #return xtool.setView()

def PlayVideo(name, url):
    xbmc.Player().PlayVideo(url)
    print "In play video: " + name + " " + url


def GetSearch(name, url):
    searchterm = xtool.getKeyboard()
    url = searchurl.format(searchterm.replace(' ', '+'))
    GetVideos(searchterm, url)

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


if __name__ == '__main__':
    allcats = dict(spankwire=[{
                                  "path": "http://www.spankwire.com/api/HubTrafficApiCall?data=searchVideos&output=json&thumbsize=small&count=100&segment=gay&search=&tags=&category=Amateur",
                                  "iconImage": "DefaultFolder.png", "thumbnailImage": "DefaultFolder.png",
                                  "label": "Amateur"
                                  },
                              {
                                  "path": "http://www.spankwire.com/api/HubTrafficApiCall?data=searchVideos&output=json&thumbsize=small&count=100&segment=gay&search=&tags=&category=Anal",
                                  "iconImage": "DefaultFolder.png",
                                  "thumbnailImage": "DefaultFolder.png",
                                  "label": "Anal"
                              },
                              {
                                  "path": "http://www.spankwire.com/api/HubTrafficApiCall?data=searchVideos&output=json&thumbsize=small&count=100&segment=gay&search=&tags=&category=Asian",
                                  "iconImage": "DefaultFolder.png",
                                  "thumbnailImage": "DefaultFolder.png",
                                  "label": "Asian"
                              },
                              {
                                  "path": "http://www.spankwire.com/api/HubTrafficApiCall?data=searchVideos&output=json&thumbsize=small&count=100&segment=gay&search=&tags=&category=Bareback",
                                  "iconImage": "DefaultFolder.png",
                                  "thumbnailImage": "DefaultFolder.png",
                                  "label": "Bareback"
                              },
                              {
                                  "path": "http://www.spankwire.com/api/HubTrafficApiCall?data=searchVideos&output=json&thumbsize=small&count=100&segment=gay&search=&tags=&category=Bears",
                                  "iconImage": "DefaultFolder.png",
                                  "thumbnailImage": "DefaultFolder.png",
                                  "label": "Bears"
                              },
                              {
                                  "path": "http://www.spankwire.com/api/HubTrafficApiCall?data=searchVideos&output=json&thumbsize=small&count=100&segment=gay&search=&tags=&category=Bi",
                                  "iconImage": "DefaultFolder.png",
                                  "thumbnailImage": "DefaultFolder.png",
                                  "label": "Bi"
                              },
                              {
                                  "path": "http://www.spankwire.com/api/HubTrafficApiCall?data=searchVideos&output=json&thumbsize=small&count=100&segment=gay&search=&tags=&category=Big Cocks",
                                  "iconImage": "DefaultFolder.png",
                                  "thumbnailImage": "DefaultFolder.png",
                                  "label": "Big Cocks"
                              },
                              {
                                  "path": "http://www.spankwire.com/api/HubTrafficApiCall?data=searchVideos&output=json&thumbsize=small&count=100&segment=gay&search=&tags=&category=Black",
                                  "iconImage": "DefaultFolder.png",
                                  "thumbnailImage": "DefaultFolder.png",
                                  "label": "Black"
                              },
                              {
                                  "path": "http://www.spankwire.com/api/HubTrafficApiCall?data=searchVideos&output=json&thumbsize=small&count=100&segment=gay&search=&tags=&category=Blowjob",
                                  "iconImage": "DefaultFolder.png",
                                  "thumbnailImage": "DefaultFolder.png",
                                  "label": "Blowjob"
                              },
                              {
                                  "path": "http://www.spankwire.com/api/HubTrafficApiCall?data=searchVideos&output=json&thumbsize=small&count=100&segment=gay&search=&tags=&category=College\\/Jocks",
                                  "iconImage": "DefaultFolder.png",
                                  "thumbnailImage": "DefaultFolder.png",
                                  "label": "College\\/Jocks"
                              },
                              {
                                  "path": "http://www.spankwire.com/api/HubTrafficApiCall?data=searchVideos&output=json&thumbsize=small&count=100&segment=gay&search=&tags=&category=Daddy\\/Mature",
                                  "iconImage": "DefaultFolder.png",
                                  "thumbnailImage": "DefaultFolder.png",
                                  "label": "Daddy\\/Mature"
                              },
                              {
                                  "path": "http://www.spankwire.com/api/HubTrafficApiCall?data=searchVideos&output=json&thumbsize=small&count=100&segment=gay&search=&tags=&category=Fetish & BDSM",
                                  "iconImage": "DefaultFolder.png",
                                  "thumbnailImage": "DefaultFolder.png",
                                  "label": "Fetish & BDSM"
                              },
                              {
                                  "path": "http://www.spankwire.com/api/HubTrafficApiCall?data=searchVideos&output=json&thumbsize=small&count=100&segment=gay&search=&tags=&category=Group",
                                  "iconImage": "DefaultFolder.png",
                                  "thumbnailImage": "DefaultFolder.png",
                                  "label": "Group"
                              },
                              {
                                  "path": "http://www.spankwire.com/api/HubTrafficApiCall?data=searchVideos&output=json&thumbsize=small&count=100&segment=gay&search=&tags=&category=Hardcore",
                                  "iconImage": "DefaultFolder.png",
                                  "thumbnailImage": "DefaultFolder.png",
                                  "label": "Hardcore"
                              },
                              {
                                  "path": "http://www.spankwire.com/api/HubTrafficApiCall?data=searchVideos&output=json&thumbsize=small&count=100&segment=gay&search=&tags=&category=HD",
                                  "iconImage": "DefaultFolder.png",
                                  "thumbnailImage": "DefaultFolder.png",
                                  "label": "HD"
                              },
                              {
                                  "path": "http://www.spankwire.com/api/HubTrafficApiCall?data=searchVideos&output=json&thumbsize=small&count=100&segment=gay&search=&tags=&category=Hentai & Anime",
                                  "iconImage": "DefaultFolder.png",
                                  "thumbnailImage": "DefaultFolder.png",
                                  "label": "Hentai & Anime"
                              },
                              {
                                  "path": "http://www.spankwire.com/api/HubTrafficApiCall?data=searchVideos&output=json&thumbsize=small&count=100&segment=gay&search=&tags=&category=Interracial",
                                  "iconImage": "DefaultFolder.png",
                                  "thumbnailImage": "DefaultFolder.png",
                                  "label": "Interracial"
                              },
                              {
                                  "path": "http://www.spankwire.com/api/HubTrafficApiCall?data=searchVideos&output=json&thumbsize=small&count=100&segment=gay&search=&tags=&category=Latino",
                                  "iconImage": "DefaultFolder.png",
                                  "thumbnailImage": "DefaultFolder.png",
                                  "label": "Latino"
                              },
                              {
                                  "path": "http://www.spankwire.com/api/HubTrafficApiCall?data=searchVideos&output=json&thumbsize=small&count=100&segment=gay&search=&tags=&category=Massage",
                                  "iconImage": "DefaultFolder.png",
                                  "thumbnailImage": "DefaultFolder.png",
                                  "label": "Massage"
                              },
                              {
                                  "path": "http://www.spankwire.com/api/HubTrafficApiCall?data=searchVideos&output=json&thumbsize=small&count=100&segment=gay&search=&tags=&category=Muscles",
                                  "iconImage": "DefaultFolder.png",
                                  "thumbnailImage": "DefaultFolder.png",
                                  "label": "Muscles"
                              },
                              {
                                  "path": "http://www.spankwire.com/api/HubTrafficApiCall?data=searchVideos&output=json&thumbsize=small&count=100&segment=gay&search=&tags=&category=Porn Stars",
                                  "iconImage": "DefaultFolder.png",
                                  "thumbnailImage": "DefaultFolder.png",
                                  "label": "Porn Stars"
                              },
                              {
                                  "path": "http://www.spankwire.com/api/HubTrafficApiCall?data=searchVideos&output=json&thumbsize=small&count=100&segment=gay&search=&tags=&category=Public",
                                  "iconImage": "DefaultFolder.png",
                                  "thumbnailImage": "DefaultFolder.png",
                                  "label": "Public"
                              },
                              {
                                  "path": "http://www.spankwire.com/api/HubTrafficApiCall?data=searchVideos&output=json&thumbsize=small&count=100&segment=gay&search=&tags=&category=Solo",
                                  "iconImage": "DefaultFolder.png",
                                  "thumbnailImage": "DefaultFolder.png",
                                  "label": "Solo"
                              },
                              {
                                  "path": "http://www.spankwire.com/api/HubTrafficApiCall?data=searchVideos&output=json&thumbsize=small&count=100&segment=gay&search=&tags=&category=Twinks",
                                  "iconImage": "DefaultFolder.png",
                                  "thumbnailImage": "DefaultFolder.png",
                                  "label": "Twinks"
                              },
                              {
                                  "path": "http://www.spankwire.com/api/HubTrafficApiCall?data=searchVideos&output=json&thumbsize=small&count=100&segment=gay&search=&tags=&category=Voyeur",
                                  "iconImage": "DefaultFolder.png",
                                  "thumbnailImage": "DefaultFolder.png",
                                  "label": "Voyeur"
                              }
                              ])
    params = parameters_string_to_dict(sys.argv[2])
    name = str(params.get("name", ""))
    url = str(params.get("url", ""))
    url = urllib.unquote(url)
    mode = str(params.get("mode", ""))
    print "Mode: " + str(mode)
    print "URL: " + str(url)
    print "Name: " + str(name)
    showContent()
    if not sys.argv[2]:
        print "ARGV[2] NONE - Calling make_viditems"
        spankwirecats = allcats.get('spankwire')
        ok = make_viditems(itemlist=spankwirecats)
        #ok = showContent()
    else:
        if mode == str(1):
            ok = GetVideos(name, url)
        elif mode == str(5):
            ok = PlayVideo(name, url)
        elif mode == str(10):
            ok = GetSearch(name, url)
    xtool.setView()

#xbmcplugin.endOfDirectory(thisPlugin, True, True, False)


#spankwirecats = []
#spankwirecats = allcats.get('spankwire')
#make_viditems(itemlist=spankwirecats)
#xbmcplugin.endOfDirectory(thisPlugin, True, True, False)

'''
params = parameters_string_to_dict(sys.argv[2])
name = str(params.get("name", ""))
url = str(params.get("url", ""))
url = urllib.unquote(url)
mode = str(params.get("mode", ""))
if not sys.argv[2]:
    ok = showContent()
else:
    if mode == str(1):
        ok = getVideos(name, url)
    elif mode == str(3):
        ok = getVideos2(name, url)
    elif mode == str(4):
        ok = getSearchQuery(name, url)
    elif mode == str(5):
        ok = getPage(name, url)  # getVideos3x
    elif mode == str(6):
        ok = getVideos4(name, url)
    elif mode == str(7):
        ok = getVideos5(name, url)

'''
