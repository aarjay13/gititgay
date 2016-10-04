from xbmcswift2 import Plugin, xbmc, ListItem, download_page, clean_dict, SortMethod
import os.path as path
import re
import urllib
import urllib2
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

plugin = Plugin()
__addondir__ = xbmc.translatePath(plugin.addon.getAddonInfo('path'))
__resdir__ = path.join(__addondir__, 'resources')
__imgsearch__ = path.join(__resdir__, 'search.png')


@plugin.route('/')
def index():
    itemsearch = {'label': 'Search', 'path': plugin.url_for(search), 'icon': __imgsearch__,
                  'thumbnail': __imgsearch__}
    item = {'label': 'Latest Episodes',
            'icon': 'DefaultFolder.png',
            'path': plugin.url_for(latest)}
    litems = []
    litems.append(item)
    litems.append(itemsearch)
    plugin.set_content('movies')
    return litems


@plugin.route('/latest')
def latest():
    url = 'http://watchseries-online.la/last-350-episodes'
    headers = {}
    headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36'})
    headers.update({
        'Accept': 'application/json,text/x-json,text/x-javascript,text/javascript,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8;charset=utf-8'})
    headers.update({'Accept-Language': 'en-US,en;q=0.5'})
    req = urllib2.Request(url=url, data=None, headers=headers)
    html = str(urllib2.urlopen(req).read())
    matches = re.compile(ur'href="(http...watchseries-online.la.episode.+?[^"])".+?</span>(.+?[^<])</a>',
                         re.DOTALL + re.S + re.U).findall(html)
    litems = []
    for eplink, epname in matches:
        epname = epname.replace('&#8211;', '-')
        spath = plugin.url_for(episode, name=epname, url=eplink)
        item = {'label': epname, 'icon': 'DefaultVideoFolder.png', 'path': spath}
        item.setdefault(item.keys()[0])
        litems.append(item)
    return litems


@plugin.route('/search')
def search():
    searchtxt = ''
    searchtxt = plugin.get_setting('lastsearch')
    searchtxt = plugin.keyboard(searchtxt, 'Search All Sites', False)
    searchquery = searchtxt.replace(' ', '+')
    plugin.set_setting(key='lastsearch', val=searchtxt)
    urlsearch = 'http://watchseries-online.la/?s={0}&search='.format(searchquery)
    headers = {}
    headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36'})
    headers.update({
        'Accept': 'application/json,text/x-json,text/x-javascript,text/javascript,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8;charset=utf-8'})
    headers.update({'Accept-Language': 'en-US,en;q=0.5'})
    req = urllib2.Request(url=urlsearch, data=None, headers=headers)
    html = unicode(urllib2.urlopen(req).read())
    # html = unicode(download_page(urlsearch))
    htmlres = unicode(html.partition('<div class="ddmcc">')[2]).split('</div>', 1)[0]
    matches = re.compile(ur'href="(http...watchseries-online.la.category.+?[^"])".+?[^>]>(.+?[^<])<.a>',
                         re.DOTALL + re.S + re.U).findall(unicode(htmlres))
    litems = []
    for slink, sname in matches:
        itempath = plugin.url_for(category, name=sname, url=slink)
        item = {'label': sname, 'icon': 'DefaultFolder.png', 'thumbnail': 'DefaultFolder.png', 'path': itempath}
        item.setdefault(item.keys()[0])
        litems.append(item)
    litems.sort(key=lambda litems: litems['label'])
    return litems


@plugin.route('/category/<name>/<url>')
def category(name, url):
    headers = {}
    headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36'})
    headers.update({
        'Accept': 'application/json,text/x-json,text/x-javascript,text/javascript,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8;charset=utf-8'})
    headers.update({'Accept-Language': 'en-US,en;q=0.5'})
    req = urllib2.Request(url=url, data=None, headers=headers)
    html = str(urllib2.urlopen(req).read())
    banner = None
    try:
        banner = str(html.split('id="banner_single"', 1)[0].rpartition('src="')[2].split('"', 1)[0])
        if banner.startswith('/'): banner = 'http://watchseries-online.la' + banner
    except:
        pass
    if banner is None: banner = 'DefaultVideoFolder.png'
    matches = re.compile(ur"href='(http...watchseries-online.la.episode.+?[^'])'.+?</span>(.+?[^<])</a>",
                         re.DOTALL + re.S + re.U).findall(html)
    litems = []
    for eplink, epname in matches:
        epname = epname.replace('&#8211;', '-')
        epath = plugin.url_for(episode, name=epname, url=eplink)
        item = {'label': epname, 'icon': banner, 'thumbnail': banner, 'path': epath}
        item.setdefault(item.keys()[0])
        litems.append(item)
    litems.sort(key=lambda litems: litems['label'])
    return litems


@plugin.route('/episode/<name>/<url>')
def episode(name, url):
    headers = {}
    headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36'})
    headers.update({
        'Accept': 'application/json,text/x-json,text/x-javascript,text/javascript,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8;charset=utf-8'})
    headers.update({'Accept-Language': 'en-US,en;q=0.5'})
    req = urllib2.Request(url=url, data=None, headers=headers)
    html = str(urllib2.urlopen(req).read())
    litems = []

    matches = re.compile(ur'href="(http...vodlocker.com.+?[^"])"', re.DOTALL + re.S + re.U).findall(html)
    if len(matches) > 0:
        matches.sort()
        umatches = list(set(matches))
    for link in umatches:
        lname = link.split('vodlocker.com/', 1)[1]
        vname = "VODLocker [COLOR green]({0})[/COLOR]".format(lname)
        vpath = 'plugin://plugin.video.hubgay/playmovie/' + urllib.quote_plus(link)
        item = {'label': vname, 'icon': 'DefaultFolder.png', 'path': vpath}  # plugin.url_for(play, url=link)}
        item.setdefault(item.keys()[0])
        litem = ListItem().from_dict(**item)
        litem.set_info(type='video', info_labels={'Title': vname})
        litem.set_is_playable(True)
        litems.append(item)

    matches = re.compile(ur'href="(http...openload.co.+?mp4)"', re.DOTALL + re.S + re.U).findall(html)
    if len(matches) > 0:
        matches.sort()
        umatches = list(set(matches))
    for link in umatches:
        lname = link.split('openload.co/f/', 1)[1]
        vid = lname.split('/', 1)[0]
        vname = 'Openload ' + lname.rpartition('/')[2][:25] + '[COLOR green](' + vid + ')[/COLOR]'
        vpath = 'plugin://plugin.video.hubgay/playmovie/' + urllib.quote_plus(link)
        item = {'label': vname, 'icon': 'DefaultFolder.png', 'path': vpath}  # plugin.url_for(play, url=link)}
        item.setdefault(item.keys()[0])
        litem = ListItem().from_dict(**item)
        litem.set_info(type='video', info_labels={'Title': vname})
        litem.set_is_playable(True)
        litems.append(item)
        # litem = ListItem(label=vname, label2=link, icon='DefaultFolder.png', thumbnail='DefaultFolder.png', path=plugin.url_for(play, url=link))
        # litem.set_is_playable = True
        # litem.set_info(type='video', info_labels={'Title': link})
        # litems.append(litem)
    litems.sort(key=lambda litems: litems['label'])
    return litems


@plugin.route('/play/<url>')
def play(url):
    # url = urllib.unquote(url)
    # plugin.set_resolved_url(url)
    # vitem = ListItem(label=url, path=url)
    # xbmc.executebuiltin('PlayMedia(%s)' % url.decode('utf-8', 'ignore'))
    # vitem.set_is_playable = True
    # vitem.set_info(type='video', info_labels={'Title' : url})
    # plugin.play_video(vitem)
    # xbmc.executebuiltin('RunPlugin(plugin://plugin.video.livestreamerkodi/play/%s)' % urllib.quote_plus(url))
    xbmc.executebuiltin('RunPlugin(plugin://plugin.video.hubgay/playmovie/%s)' % urllib.quote_plus(url))
    return [plugin.set_resolved_url(url)]
    # plugin.set_resolved_url(url)
    # xbmc.Player().play(url)
    # return plugin.finish(items=plugin.set_resolved_url(url))
    # plugin.play_video(url)
    # plugin.play_video(urllib.unquote(url))
    # plugin.play_video(item=ListItem(label=url, path=url))


if __name__ == '__main__':
    plugin.run()
    plugin.set_content('movies')
    plugin.set_view_mode(0)
