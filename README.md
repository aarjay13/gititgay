# kodi-repo-gaymods
Adult repo for Gay Specific Addons for Kodi _XBMC_ **(Jarvis 16.0+)** 

Intended to be the one stop place for the latest addons and most up to date code for addons that will display gay content from adult websites typically forked addons already written for many straight sites but modified slightly to filter out content that is not GAY 
## WORKING ADDONS
__(updated 13 March 2016)__

- plugin.video.gayuwc
- plugin.video.dagay

## BROKEN ADDONS 
__(updated 13 March 2016)__

- plugin.video.gayboystube
- plugin.video.largecamtube

## Latest News
_(updated 13 March 2016)_

I am working on fixing the modifications I have made to addons for gay content filtering or the feature improvements to the GayBoysTube, GayPornium, and a forked version of the devientclip addon to scrape their gay site, DaGay, on here and tested on Jarvis and install and run correctly if installed from this repository. I had these individually working locally as zip files but they aren't working or installing via this repo (which is the first repository I have attempted and my python is getting better but been a case of learning by doing for the past year)
All that said as I had about 5 addons working on Jarvis RC's after taking a break from stuff for the past couple months and trying to move them into a repo instead of just standalone zip files seems to have broken something but likely a minor problem that I hope to solve shortly and distinguish the addons that I believe to be working at the top of this page and in the changelogs/addons details
Some additional minor tweaks to python code / updates for Jarvis have been made to some addons as well.

## Goals and Intentions
I ultimately wanted to try and centralize gay video addons into one repo which I would happily see branch off the wonderful XBMCADULT repo which could allow installing the Gay XBMCADULT repo from their main repo, also allowing the few gay specific plugins already in that repo like xHamsterGay and others (many of which don't fully work, or lack functionality) and remove them from the main repo and move to the Gay XBMCADULT repo instead. Whether this ever would happen or not isn't important to me, but what is will be having a centralized repo that users and developers can find gay adult oriented addons. I hope that by putting them all in one spot with more updated code and additional functionality will encourage others to contribute other adult addons that are simple to modify to grab gay content to this central spot. I also hope that the code changes and standards could be pushed back to the original repo's hosting them so everyone can benefit from user to developers by building off these code updates. Or possibly removing the older versions from their repo and add this repo's installer keeping one main repo for forks of all the gay addons. Hopefully this can lead to fixing up broken addons, standardizing settings, and a more extensive selection of gay addons and keep up with how many str8 addons are around. 
- Repository for Kodi (XBMC) Video Addons for Gay XXX 18+ mainly existing Addons from other adult repos but ones that lacked any GAY category/filtering of video's from the straight ones focusing on plugins for sites that contain gay content and require only minor code additions to display either gay or straight results depending on the selected addon's filter setting.
- I also have included existing gay plugins from AGX, XBMCADULT, and other REPO's some of which haven't worked for a while, other's such as the GayBoysTube addon worked fine for basic display of new videos, and random, and just need some additional functionality added to them like Category's, Search and last search, Download context Menu actions, and sorting options.
- My first goals are to have the addons already working that are gay specific or have gay categories already, copied to this repo
- I wrote very little of the code found here. Praise to authors of the original code base I simply used based python knowledge to make sure gay content was being scraped, and was seperated from str8 results/tranny categories. Most of the changes are simple a long IF statement to find some keywords and to not add results containing other clearly str8 female results.
- All of this is a work in progress some I still have errors and no results. This is my first attempt at a proper repo and not just some little code changes so please understand and help where you see any errors!
- I hope that many of these addons could be merged back in with their original code one day and simply have a gay/straight/keywords settings included with each of the addons settings.xml and if settingGay is True then the small code changes/standard filter functions are executed before items get added to an xbmc directory list.
- For now I am just trying to get as many of these addons in one place and renamed so that these code changes can be added and tested and all in one repo as xbmcadult repo has many in various states, UWC, PODGOD, the UWC repo I would like to raise some major issues with later!

## CURRENT TODO
- Add a resources folder for all addons with a generic settings.xml with standardized naming conventions
- Implement in settings.xml for all addons a Gay Filter on BOOL, a Last Search TEXT, a list of sorting options for results
- Implement standard python code for reading/setting the settings.xml from Addon, and a showSearch that will display the keyboard with the last search as read from settings as well as then updating that value on return.
- Implement a modified addDirectoryItem function that can check to see if GAY filter is on and add/filter out items based on that.
- Implement a standard list of straight and gay keywords to be used by the filters if a site doesn't specifically have gay categories or if additional filtering of results is desired such as ones set by the user in the addons settings.

## DEFAULT SETTINGS.XML
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

## UltimateWhiteCream now gayUWC
I have forked the latest version of UWC code and renamed the addon for the time being to plugin.video.gayuwc
- This addon seems to be getting a load of updates and new sites and functionality added all the time.
- The code is vast and unlike videodevil which attempts to sort of handle the scraping through it's own config/catcher/regex's the UWC leaves it to each sites functionality is a python file.
- This is fine, and as a programmer I like this more as I can easily look at and change and fix problems I see with any of the UWC site python files without having to try and learn a cfg/catcher/regex format which also seems to be splintered among many different forks of video devil making it even worse as videodevil cfg/catcher/list files don't all work on dif versions as they atttempted to add new keywords, functions, etc.
- My PROBLEM though is that UWC which is really cool has a real lack of any gay filtering ability, and when it does exist it tends to be gay/tranny.
- I have found code that even went so far as to say if the result contained the word gay don't include it!
- I REALLY would love to see a solution that wouldn't require constant comparing and modifying of the UWC files and try to get them on board with the simple suggested GAY boolean setting I set out above and start trying to get the site specific python files to check this gay boolean value and apply it where the site has a gay category. At the moment it's a real nightmare and shocking to see statements in code like if not name.startswith('gay'): add(name) without giving the user the option to say they want these gay options or perhaps only these. 

# ABOUT ME
- Jeremy j@alljer.com
- [CryptoCoins.Com](http://www.cryptocoins.com/) Founder (HELP INVESTMENT NEEDED)

