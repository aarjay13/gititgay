#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os, os.path
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, xbmcvfs
import urllib, urllib2
from urllib import quote_plus, unquote_plus, basejoin
from urllib2 import Request, urlopen

class xbmcUtils(object):
    #######################################
    # Xbmc Helpers
    #######################################
    def __init__(self, addonid='plugin.video.motherless', pluginhandle=None):
        self.handle = int(sys.argv[1])
        if pluginhandle is not None:
            self.handle = pluginhandle
        self.std_headers = {
            'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.6) Gecko/20100627 Firefox/3.6.6',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',}
        self.req = Request(url="http://www.gaypornium.com/{0}", headers=self.std_headers)
        if addonid != 'plugin.video.':
            self.addon = xbmcaddon.Addon(id=str(addonid))
            self.addonid = str(addonid)
        else:
            self.addon = xbmcaddon.Addon()
            self.addonid = str(self.addon.getAddonInfo('id'))
        self.resDir = os.path.join(xbmc.translatePath(self.addon.getAddonInfo('path').decode('utf-8')), "resources/")
        self.profile = xbmc.translatePath(self.addon.getAddonInfo('profile').decode('utf-8'))
        self.cleanStringMethod = staticmethod(self.removeNonAscii)


    def getUrl(self, url):
        assert isinstance(self.req, Request)
        self.req.url = urllib2.toBytes(url)
        response = urlopen(self.req)
        link = response.read()
        response.close()
        return self.removeNonAscii(link)

    def removeNonAscii(self, s):
        return "".join(filter(lambda x: ord(x) < 128, s))

    def addLink(self, videourl, name, iconimage='DefaultVideo.png', fanart=None, plot='', genre='', duration='', mode='5', returnItem=False):
        try: name = name.encode('utf-8')
        except: pass
        namesafe = quote_plus(name)
        pathurl = 'plugin://{0}/?mode=playVideo&url={1}'.format(self.addonid, videourl)
        dlaction = "XBMC.RunPlugin('plugin://script.module.youtube.dl/?url={0}')".format(videourl) #home/addons/script.module.youtube.dl/lib/youtube_dl/__main__.py?{0}')".format(videourl)
        ctx =[(('[COLOR red]Download Video[/COLOR]', dlaction))]
        #ctx =[(('[COLOR red]Download Video[/COLOR]', 'XBMC.RunPlugin({0}?url={1}&mode=21&name={2})'.format(sys.argv[0], videourl, namesafe)))]
        #u = pathurl + "?url={0}&mode={1}".format(quote_plus(videourl), str(mode))
        infolbl = {"Title": name, "Plot": plot, "Genre": genre, "Duration": duration}
        liz = xbmcgui.ListItem(label=name, iconImage=iconimage, thumbnailImage=iconimage, path=videourl)
        liz.setInfo(type="Video", infoLabels=infolbl)
        liz.setProperty('IsPlayable', 'true')
        liz.addContextMenuItems(items=ctx, replaceItems=False)
        if fanart is not None: liz.setProperty("Fanart_Image", fanart)
        if returnItem:
            return (self.handle, pathurl, liz, 1)
        else:
            return xbmcplugin.addDirectoryItem(handle=self.handle, url=pathurl, listitem=liz, totalItems=1)

    def addListItem(self, liz, pathurl):
        return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=pathurl, listitem=liz, totalItems=1)

    def select(self, title, menuItems):
        select = xbmcgui.Dialog().select(title, menuItems)
        if select == -1:
            return None
        else:
            return menuItems[select]

    def getKeyboard(self, default='', heading='', hidden=False):
        kboard = xbmc.Keyboard(default, heading, hidden)
        kboard.doModal()
        if kboard.isConfirmed():
            return kboard.getText()
        return ''

    def setView(self, viewMode=500, endofdir=True):
        #xbmcplugin.addSortMethod(handle=self.handle, sortMethod=xbmcplugin.SORT_METHOD_LABEL)
        self.setSortMethodsForCurrentXBMCList(sortKeys=['name', 'date','file','duration', 'none'])
        if not endofdir:
            xbmc.executebuiltin("Container.SetViewMode({0})".format(viewMode))
        else:
            ok = xbmcplugin.endOfDirectory(self.handle)
            xbmc.executebuiltin("Container.SetViewMode({0})".format(viewMode))
            return ok

    def getImage(self, title):
        dialog = xbmcgui.Dialog()
        image = dialog.browse(1, title, 'pictures', '.jpg|.png', True)
        return image

    def showMessage(self, msg):
        xbmc.executebuiltin('Notification(Motherless,' + str(msg.encode('utf-8', 'ignore')) + ')')

    def showBusyAnimation(self):
        xbmc.executebuiltin('ActivateWindow(busydialog)')

    def hideBusyAnimation(self):
        xbmc.executebuiltin('Dialog.Close(busydialog,true)')

    def closeAllDialogs(self):
        xbmc.executebuiltin('Dialog.Close(all, true)')

    def log(self, msg):
        try:
            xbmc.log(msg)
        except:
            xbmc.log(msg.encode('utf-8'))

    def addSortMethod(self, method):
        xbmcplugin.addSortMethod(handle=self.handle, sortMethod=method)

    def setSortMethodsForCurrentXBMCList(self, sortKeys):
        if not sortKeys or sortKeys == []:
            self.addSortMethod(xbmcplugin.SORT_METHOD_UNSORTED)
        else:
            if 'name' in sortKeys:
                self.addSortMethod(xbmcplugin.SORT_METHOD_LABEL)
            if 'size' in sortKeys:
                self.addSortMethod(xbmcplugin.SORT_METHOD_SIZE)
            if 'duration' in sortKeys:
                self.addSortMethod(xbmcplugin.SORT_METHOD_DURATION)
            if 'genre' in sortKeys:
                self.addSortMethod(xbmcplugin.SORT_METHOD_GENRE)
            if 'rating' in sortKeys:
                self.addSortMethod(xbmcplugin.SORT_METHOD_VIDEO_RATING)
            if 'date' in sortKeys:
                self.addSortMethod(xbmcplugin.SORT_METHOD_DATE)
            if 'file' in sortKeys:
                self.addSortMethod(xbmcplugin.SORT_METHOD_FILE)
            if 'none' in sortKeys:
                self.addSortMethod(xbmcplugin.SORT_METHOD_UNSORTED)

    def getContainerFolderPath(self):
        return xbmc.getInfoLabel('Container.FolderPath')

    def getListItemPath(self):
        return xbmc.getInfoLabel('ListItem.Path')

    def getCurrentWindow(self):
        return xbmc.getInfoLabel('System.CurrentWindow')

    def getCurrentControl(self):
        return xbmc.getInfoLabel('System.CurrentControl')

    def getCurrentWindowXmlFile(self):
        return xbmc.getInfoLabel('Window.Property(xmlfile)')
