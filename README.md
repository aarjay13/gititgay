## repository.gaymods
###  A Collection of Gay Adult addons for ~~XBMC~~ Kodi *(Jarvis 16.0+)* all in one place 
Intended to be the one stop place for the latest addons and most up to date code for addons that will display gay content from adult websites typically forked addons already written for many straight sites but modified slightly to filter out content that is not GAY 
#### STATUS OF PLUGINS
*updated 13 March 2016*

- [x] plugin.video.gayuwc (*__status:__ See below for more details on areas I could use help with such as porndig.py* 14/3/16)
- [x] plugin.video.gayboystube (*__status:__ Worked with Latest Videos, or Random have added categories, sorting, and searching * 14/3/16)
- [x] plugin.video.dagay (*__status:__ Uses the dclip code to run as they are from the same company * 14/3/16)
- [x] plugin.video.largecamtube (*__status:__ Sorted categories that are gay to top and any category attempts to sort the videos in that category by gay ones at top of list * 14/3/16)
- [x] plugin.video.gaypornium (*__status:__ Worked with Latest Videos, or Random have added categories, sorting, and searching * 14/3/16)
- [x] plugin.video.dclip (*__status:__ DevientClip has a small set of sites all with same templates so scraping the gay site was as easy as setting it to the URL and it just worked which spawned the video.DaGay plugin but I left options in the dclip addon to set gay or straight so it essentially can be all put together one day * 14/3/16)
- [ ] plugin.video.oxo (*__status:__ Not Started * 14/3/16)
- [ ] plugin.video.xhamstergay (*__status:__ Not Started From XBMCADULT repo lacks functionality and fails to return items * 14/3/16)
- [ ] plugin.video.youporngay (*__status:__ Not Started From XBMCADULT repo lacks functionality and fails to return items * 14/3/16)
- [ ] plugin.video.youjizzgay (*__status:__ Not Started From XBMCADULT repo lacks functionality and fails to return items * 14/3/16)
- [ ] plugin.video.motherless (*__status:__ Not started * 14/3/16)
- [ ] plugin.video.xstream (*__status:__ I had modified the gstream.to file to filter the gay/tranny section but I think the site has been blocked as it stopped working so this may be removed soon I have instead used UWC's Pornhive and Paradisehill Plugins much to the same results as I had from gstream when it worked * 14/3/16)

## Latest News
_(updated 13 March 2016)_

- I am working on fixing the modifications I have made to addons for gay content filtering or the feature improvements to the GayBoysTube, GayPornium, and a forked version of the devientclip addon to scrape their gay site, DaGay, on here and tested on Jarvis and install and run correctly if installed from this repository. I had these individually working locally as zip files but they aren't working or installing via this repo (which is the first repository I have attempted and my python is getting better but been a case of learning by doing for the past year)
- All that said as I had about 5 addons working on Jarvis RC's after taking a break from stuff for the past couple months and trying to move them into a repo instead of just standalone zip files seems to have broken something but likely a minor problem that I hope to solve shortly and distinguish the addons that I believe to be working at the top of this page and in the changelogs/addons details
Some additional minor tweaks to python code / updates for Jarvis have been made to some addons as well.

## Goals and Intentions
- I ultimately wanted to try and centralize gay video addons into one repo which I would happily see branch off the wonderful XBMCADULT repo which could allow installing the Gay XBMCADULT repo from their main repo, also allowing the few gay specific plugins already in that repo like xHamsterGay and others (many of which don't fully work, or lack functionality) and remove them from the main repo and move to the Gay XBMCADULT repo instead. Whether this ever would happen or not isn't important to me, but what is will be having a centralized repo that users and developers can find gay adult oriented addons. I hope that by putting them all in one spot with more updated code and additional functionality will encourage others to contribute other adult addons that are simple to modify to grab gay content to this central spot. I also hope that the code changes and standards could be pushed back to the original repo's hosting them so everyone can benefit from user to developers by building off these code updates. Or possibly removing the older versions from their repo and add this repo's installer keeping one main repo for forks of all the gay addons. Hopefully this can lead to fixing up broken addons, standardizing settings, and a more extensive selection of gay addons and keep up with how many str8 addons are around. 
- All of this is a work in progress and attempt to get a full list and status together which is why plugins have been hard forked until the status of them can be determined. 
- This is my first attempt at a proper repo and I am not the best python programmer so all help is welcome.
- I will work on tracing the origins of plugins to repo's and authors along the way and update this info in the status of these addons but very little of the code is written by me I have simply tried to add functions and fixes to already existing addons written by other's who I thank and hope will be interested in the changes I have implemented. 
- Creating hard forks of any existing Gay addons from any repo I have found them on and in working and non working states to get a complete picture of what needs fixing, what needs functionality additions, and what works fine already and listing those statuses so everyone can see what still needs fixing and hopefully help.
- Some of the repo's that I found gay plugins in are PODGOD, AGX, XBMCADULT, I will try to get a better list together soon. 
- Once a plugin runs and has the standardized functions and settings included the status can be updated on the repo, changelog, and in the addons.xml metadata then I would hope to submit it back to original repository for updating and/or adding this repo so that users can keep updated versions.
- Many plugins should be able to function as str8 or gay with the user being able to set this in settings, I hope that pushing code updates to some of the existing adult repo's with a sexual orientation setting of BOOL settingGay could become more prevelent in all adult plugins so everyone can benefit from developers hard work on these addons not just those seeking straight porn. 
- Ugly filters could be more easily added to plugins in the xbmc.addDirectoryItem() by calling a simple in between function call if the settingGay is True then run the name of the item against a list of gay terms to see if any match and if they do return it to the addDirectoryItem otherwise next. Not an ideal solution but a quick dirty fix for sites lacking gay categories.

### CURRENT TODO
- Add a resources folder for all addons with a generic settings.xml and a set of standard settings and names
- Gather a full list of addons, where they came from, the version they are hard forked from, if they are working, and suggested TODOs for them.
- Make sure all addons have updated changelogs and metadata in their addon.xml to distinguish them from the version they were hard forked from so that merging them back to the original repo could be possible.
- Implement a settings.xml for all addons full details below on field names so that the same python code can be used on each plugin to perform initial setting of variables and the same doSearch, doFilter, and other functions will require as little customization as possible from one plugin to another.
- Implement a modified addDirectoryItem function that can check to see if GAY filter is on and add/filter out items based on that.
- Implement a standard list of straight and gay keywords to be used by the filters if a site doesn't specifically have gay categories or if additional filtering of results is desired such as ones set by the user in the addons settings.

#### DEFAULT SETTINGS.XML
Suggested defaults for all addons which may or may not have code implemented for handling all settings initially but hope to have standard functions to make adding functionality to addons easy by just needing to know where to call the functions such as a startup, dosearch, dofilter in a function about to call addDirectoryItem, etc.
Python code would use xbmcaddon.Addon object's getSetting function to set variables in setup routine such as dofiltergay = bool(unicode(Addon.getSetting(id='settingGay')))

- settingGay (BOOL) if TRUE then filter out straight/female videos and attempt to show male gay porn results.
- settingPages (BOOL) if TRUE then rather than paginating 6 pages with a next page retrieve and scrape all results and combine to one results page. Could cause slower machines problems if many hundreds of items are added with thumbnails to load remotely etc.
- settingSearch (TEXT) The last search string the user typed into the keyboard upon selecting a search option, keyboard will default to this text.
- settingSortby (LABELENUM|TEXT) A list of possible sorting orders to pass in the url to scrape as some may want by most recently added, other sites may allow sorting by number of views, popularity, name, most default to newest by date but useful to sometimes see results in another order.
- settingFilterwords (TEXT) User specified additional words that will be used to decide whether a result is included or not
- settingNofilter (BOOL) Default true so user keywords will not be used if FALSE then read words to filter by and find out if filter is remove any results that DO contain these words or filter results that MUST contain these keywords. Only used for Videos not categories or directories
- settingFilteroper (LABELENUM|TEXT) "Remove Items That Contain Keywords" or "Show Only Items With Keywords"

```
<settings>
	<category label="General">
		<setting id="settingGay" label="Gay Filter (Uncheck for Straight)" values="true" default="true" type="bool" visible="true" />	
		<setting id="settingPages" label="Multipage Results (Uncheck to Paginate)" values="true" default="true" type="bool" visible="true" />
		<setting id="settingSearch" label="Last Search" values="" default="" type="text"  visible="true" />
		<setting id="settingSortby" label="Sort Method" values="recent|rated|viewed|popular|title|longest" default="recent" type="labelenum" visible="true" />
		<setting id="settingNofilter" label="Do Not Use Keyword Filtering" values="true" default="true" type="bool" visible="true" />
		<setting id="settingFilterwords" label="Keywords (space seperated)" values="" default="" type="text" visible="true" />
		<setting id="settingFilteroper" label="Filter keywords by" values="Remove If Keyword Found|Show Only Results Matching a Keyword" default="Show Only Results Matching a Keyword" type="labelenum" visible="true" />
	</category>
</settings>
```
- Implement standard python code for reading/setting these values which the user has set as well as functions to present a search keyboard with the last search as well as updating it after a search, filterItem to be called before an item is added using xbmc.addDirectoryItem if the settingNoFilter is False or the settingGay is True, etc..

### UWC UltimateWhiteCream now gayUWC

gayUWC was hard forked from uwc plugin V 1.0.95 many of the sites it uses have no gay content at all
Pornhive and paradisehill have gay/tranny categories which I have attempted to filter in the python code for those sites but it is very ugly code and needs to think about pagination and retrieving more than one page at a time. 
- pornhive.py
- paradisehill.py

#### TODO: porndig.py
- I am not sure what other plugins could be modified but I have seen that porndig has gay categories and even offers options of Pro or Amateur which it looks at on it's startup, so having it also check for Gay on startup is easy enough but I haven't been able to use the existing functions with the gay URLs and have it return any items but it should be an easy enough thing to accomplish for someone a bit more experienced at Python/Kodi/UWC's standard functions.  Below are my suggestions and URL's to the gay content on porndig.
- porndig.py (default.py calls this module so by adding a third porndig choice to the default.py called Porndig Gay you could then update the below code to look for Gay in the name:

```
if 'Amateurs' in name:
    addon.setSetting('pdsection', '1')
else:
    addon.setSetting('pdsection', '0')
```
If the above code checked for Gay and set the pdsection setting to 2 then with a few additional tweaks to the module it should be able to use most of it's existing code to scrape the gay content on the following URLS:

- http://www.porndig.com/gays
- http://www.porndig.com/gay/videos/
- http://www.porndig.com/gay/studios/
- http://www.porndig.com/gay/pornstars/
- http://www.porndig.com/channels/1045/amateur-gay *Category url for gay content all ends with -gay as this url is an example of*

I made attempts to make the modifications but failed to work which I think is down to not fully understanding the parameters to pass to the functions which put the full URL together so I think that I'm not setting a base url correctly or the channel number, etc so if anyone wants to try to implement this correctly would be great. I think starting with changing how the pdsection setting is set and adding a new entry to the default.py for Porndig Gay as follows:

```
utils.addDir('[COLOR hotpink]Porndig[/COLOR] [COLOR white]Gay[/COLOR]','http://www.porndig.com/gay',290,os.path.join(imgDir, 'porndig.png'),'')
utils.addDir('[COLOR hotpink]Porndig[/COLOR] [COLOR white]Professional[/COLOR]','http://www.porndig.com',290,os.path.join(imgDir, 'porndig.png'),'')
utils.addDir('[COLOR hotpink]Porndig[/COLOR] [COLOR white]Amateurs[/COLOR]','http://www.porndig.com',290,os.path.join(imgDir, 'porndig.png'),'')
```
Next if the porndig.py file looks for Gay in the name you will know the gay directory was selected but it's all the code after that checks the pdsection setting that I don't know how to make work with the above gay URLS

```
if 'Amateurs' in name: addon.setSetting('pdsection', '1')
elif 'Gay' in name: addon.setSetting('pdsection', '2')
else: addon.setSetting('pdsection', '0')
```
This is where I haven't gotten past yet, need to handle anywhere pdsection is checked to now handle the gay option of 2 with the correct gay url's and parameters. 

## ABOUT ME
- Author: Jeremy j@alljer.com
- Founder: [CryptoCoins.Com](http://www.cryptocoins.com/) Physical CryptoCurrency Worth Holding Onto

