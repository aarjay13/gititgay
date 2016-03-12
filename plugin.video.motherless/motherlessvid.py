import sys, os, os.path, urllib, urllib2, urlparse
from urllib import basejoin, quote_plus, unquote_plus

MotherlessList = []

class MotherlessVid(dict):

    def __init__(self, **kwargs):
        """
        : attribute member : MotherlessVid.Member
        : attribute thumbnail : string
        : attribute time : string
        : attribute mediatype : string
        : attribute title : string
        : attribute size : MotherlessVid.Size
        : attribute bytes : string
        : attribute link : string
        : attribute codename : string
        : attribute tags : listt
        """
        try:            
            super(MotherlessVid, self).__init__(**kwargs)
            self.VHost = "http://cdn.videos.motherlessmedia.com/videos/{0}.mp4"
            self._tags = []
            self._size = MotherlessVid._Size() 
            self._member = MotherlessVid._Member()
            assert isinstance(self._size, MotherlessVid._Size)
            assert isinstance(self._member, MotherlessVid._Member)
            if self.has_key("title") == False:
                self.update(**kwargs)
            if self.has_key("tags"):
                self._tags = self.get("tags")
            elif kwargs.has_key("tags"):
                self._tags = kwargs.get("tags")
                self.update(tags=self._tags)
            if kwargs.has_key("size"):
                self._size = MotherlessVid._Size(**kwargs.get("size"))
            elif self.has_key("size"):
                self._size = MotherlessVid._Size(**self.get("size"))
            if kwargs.has_key("member"):
                self._member = MotherlessVid._Member(**kwargs.get("member"))
            elif self.has_key("member"):
                self._member = MotherlessVid._Member(**self.get("member"))
            if self.has_key("link"):
                idvid = str(str(self.get("link")).rpartition('/')[2])
                newlink = str(basejoin("http://motherless.com/", idvid))
                vlink = str(self.VHost.format(idvid))
                self.update(vpath=vlink, link=vlink, path=newlink)
            if self.has_key("codename"):
                vpath = str(self.VHost.format(str(self.get("codename"))))
                self.update(vpath=vpath, link=vpath)
        except:
            print ("Failed to init variables of MotherlessVid {0} {1}".format(str(kwargs), str(self.__dict__)))
        
    @property
    def label(self):
        return "{0} ({1}s) ".format(str(self.get("title")).title(), str(self.get("size").seconds))

    @property
    def label2(self):
        return "[{0}] {1}".format(str(' ').join(self.get("tags")).title(), str(self.get("codename")).upper())

    @property
    def path(self):
        return str(self.get("path"))

    @property
    def vpath(self):
        return str(self.get("vpath"))

    @property
    def thumbnail(self):
        return str(self.get("thumbnail"))

    @property
    def url(self):
        if self.has_key("link"):
            return str(self.get("link"))
        else:
            u = self.VHost.format(self.get("codename"))
            if u is not None:
                self.update(link=str(u))
            else:
                u = str(self.VHost.format(str(self.get("path")).rpartition('/')[2]))
                self.update(link=u)
        return u

    @property
    def link(self):
        return self.url

    @link.setter
    def link(self, value):
        u = str(value)
        newlink = basejoin("http://motherless.com/", str(str(u).rpartition('/')[2]))
        self.update(link=newlink)


    @property
    def codename(self):
        return self.get("codename")

    @codename.setter
    def codename(self, value):
        self.update(codename=value)

    @property
    def bytes(self):
        return self.get("bytes")

    @bytes.setter
    def bytes(self, value):
        self.update(bytes=value)

    @property
    def tags(self):
        return self.get("tags")

    @tags.setter
    def tags(self, value):
        self.update(tags=value)

    @property
    def title(self):
        return self.get("title")

    @title.setter
    def title(self, value):
        self.update(title=value)

    @property
    def mediatype(self):
        return self.get("mediatype")

    @mediatype.setter
    def mediatype(self, value):
        self.update(mediatype=value)

    @property
    def time(self):
        return self.get("time")

    @time.setter
    def time(self, value):
        self.update(time=value)

    class _Member(object):

        def __init__(self, **values):
            if values is not None:
                self._memberdict = values
            self._username = None
            self._tagline = None
            self._profile = None
            self._avatar = None            
            for k, v in enumerate(self._memberdict):
                self._setKey(str(k), v)

        def _setKey(self, key, val):
            ok = False
            if key.find('username') != -1:
                self._username = val
                ok = True
            elif key.find( 'tagline') != -1:
                self._tagline = val
                ok = True
            elif key.find( 'profile') != -1:
                self._profile = val
                ok = True
            elif key.find( 'avatar') != -1:
                self._avatar = val
                ok = True
            if ok:
                self._memberdict.update(key=val)
            return ok

        @property
        def asDict(self):
            return self._memberdict

        @asDict.setter
        def asDict(self, value):
            try:
                if value is not None:
                    for k, v in enumerate(value):
                        self._setKey(key=str(k), val=v)
            except:
                self._memberdict.update(value)

        @property
        def username(self):
            try:
                self._username = self._memberdict.get("username")
            except:
                self._setKey("username", self._username)
            return self._username

        @username.setter
        def username(self, value):
            self._memberdict.update(username=value)
            self._setKey("username", value)

        @property
        def tagline(self):
            return self._memberdict.get("tagline")

        @tagline.setter
        def tagline(self, value):
            self._memberdict.update(tagline=value)
            self._setKey("tagline", value)

        @property
        def profile(self):
            return self._memberdict.get("profile")

        @profile.setter
        def profile(self, value):
            self._memberdict.update(profile=value)
            self._setKey("profile", value)

        @property
        def avatar(self):
            return self._memberdict.get("avatar")

        @avatar.setter
        def avatar(self, value):
            self._memberdict.update(avatar=value)
            self._setKey("avatar", value)


    @property
    def member(self):
        if self.has_key("member"):
            return  self.get("member")
        else:
            return self._member

    @member.setter
    def member(self, **values):
        try:
            if self.has_key("member"):
                self.get("member").update(values)
            else:
                self.update(member=values)
        except:
            self._member = MotherlessVid._Member(values=values)
            self.update(members=self._member.asDict)

    @property
    def size(self):
        if self._size is not None:
            return self._size
        else:
            if self.has_key("size"):
                return self.get("size")

    @size.setter
    def size(self, **values):
        self._size = MotherlessVid._Size(**values)
        self.update(size=self._size)

    class _Size(object):

        def __init__(self, **values):
            """
            : attribute width : string
            : attribute seconds : string
            : attribute height : string
            """
            if values is not None:
                self._sizedict = values            
            self._width = None
            self._seconds = None
            self._duration = None
            self._height = None            
            for k, v in enumerate(self._sizedict):
                self._setKey(str(k), v)

        def _setKey(self, k, v):
            ok = False
            if k.find('width') != -1:
                self._width = v
                ok = True
            elif k.find('seconds') != -1:
                self._seconds = v
                ok = True
            elif k.find('duration') != -1:
                self._duration = v
                ok = True
            elif k.find('height') != -1:
                self._height = v
                ok = True
            if ok:
                self._sizedict.update({k: v})
            if self._sizedict.get('duration') is None and self._seconds is not None:
                self._duration = str(self._setDuration(seconds=int(self._sizedict.get("seconds"))))
                self._sizedict.update({"duration": self._duration})

        def _setDuration(self, seconds, strvalue=None):
            if strvalue is not None:
                self._duration = str(strvalue)
            elif seconds is not None and str(seconds).isdigit():
                self._seconds = seconds
                h, m, s = 0,0,int(seconds)
                if s > 3600:
                    h = (s/3600).numerator()
                    s = s - (3600*h)
                if s > 60:
                    m = (s/60).numerator()
                    s = s - (60*m)
                if h > 0:
                    self._duration = "{0}h:{1}m:{2}s".format(str(h), str(m), str(s))
                elif m > 0:
                    self._duration = "{0}m:{2}s".format(str(m), str(s))
                else:
                    self._duration = "{0}s".format(str(s))
            self._sizedict.update({"duration": self._duration})
            return self._duration

        @property
        def seconds(self):
            return self._sizedict.get("seconds")

        @seconds.setter
        def seconds(self, value):
            self._seconds = value
            self._duration = self._setDuration(seconds=value)
            self._sizedict.update({"seconds": self._seconds, "duration": self._duration})

        @property
        def duration(self):
            return self._sizedict.get("duration")

        @duration.setter
        def duration(self, value):
            self._duration = value
            self._sizedict.update({"duration": self._duration})

        @property
        def width(self):
            return self._sizedict.get('width')

        @width.setter
        def width(self, value):
            self._width = value
            self._sizedict.update({"width": self._width})

        @property
        def height(self):
            return self._sizedict.get('height')

        @height.setter
        def height(self, value):
            self._height = value
            self._sizedict.update({"height": self._height})


