# -*- coding: utf-8 -*-

'''
    Funimation|Now Add-on
    Copyright (C) 2016 Funimation|Now

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import sys;
import urlparse;
import logging;

from resources.lib.modules.log_handler import LogHandler;


def setup_logging():
    import xbmcaddon;
    
    addon = xbmcaddon.Addon();

    log_level = (int(addon.getSetting('loglvl')) + 1) * 10;
    logger = logging.getLogger('funimationnow');

    logger.setLevel(log_level);

    formatter = logging.Formatter('[{0}] %(funcName)s : %(message)s'.format(addon.getAddonInfo('id')));
    lh = LogHandler();

    lh.setLevel(log_level);
    lh.setFormatter(formatter);

    logger.addHandler(lh);

    return logger;

logger = setup_logging();
#logger.error('ARGV: %s', sys.argv);

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')));

action = params.get('action');
name = params.get('name');
title = params.get('title');
year = params.get('year');
imdb = params.get('imdb');
tvdb = params.get('tvdb');
season = params.get('season');
episode = params.get('episode');
tvshowtitle = params.get('tvshowtitle');
premiered = params.get('premiered');
url = params.get('url');
image = params.get('image');
meta = params.get('meta');
select = params.get('select');
query = params.get('query');
source = params.get('source');
content = params.get('content');
filtertype = params.get('filtertype');

'''
logger.error('------------------------------------------------------------------')
logger.error(action)
logger.error('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
logger.error(params)
logger.error('------------------------------------------------------------------')
'''


if action == None:
    from resources.lib.indexers import navigator;

    navigator.navigator().root();

elif action == 'authTrakt':
    from resources.lib.modules import trakt;

    trakt.authTrakt();

elif action == 'featured':
    from resources.lib.indexers import navigator;

    navigator.navigator().filtered(action, filtertype, params);    

elif action == 'showsNavigator':
    from resources.lib.indexers import navigator;
    
    navigator.navigator().tvshows();

elif action == 'browseNavigator':
    from resources.lib.indexers import navigator;
    
    navigator.navigator().browse();

elif action == 'alphaNavigator':
    from resources.lib.indexers import navigator;
    
    navigator.navigator().browsealpha();

elif action == 'getAllRatings':
    from resources.lib.indexers import navigator;

    navigator.navigator().ratings(action);

elif action == 'genres':
    from resources.lib.indexers import navigator;

    navigator.navigator().genres(action);

elif action == 'extras':
    from resources.lib.indexers import navigator;

    navigator.navigator().filtered(action, filtertype, params, filtertype);

elif action == 'shows':
    from resources.lib.indexers import navigator;

    navigator.navigator().filtered(action, filtertype, params);

elif action == 'getVideoHistory':
    from resources.lib.indexers import navigator;

    navigator.navigator().filtered(action, filtertype, params);

elif action == 'getQueue':
    from resources.lib.indexers import navigator;
    #import xbmcgui;

    #logger.error(xbmcgui.getCurrentWindowId())
    
    '''import json;
    from resources.lib.modules import control;

    #http://forum.kodi.tv/showthread.php?tid=162162
    #lib = control.jsonrpc('{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": {"properties" : ["imdbnumber", "title", "year"]}, "id": 1}')
    logger.error('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    logger.error('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    #lib = control.jsonrpc('{ "jsonrpc": "2.0", "method": "JSONRPC.Introspect", "params": { "filter": { "id": "Favourites.AddFavourite", "type": "method" } }, "id": 1 }')

    lib = control.jsonrpc('{"jsonrpc": "2.0", "method": "Favourites.AddFavourite", "params": {"title":"MYFAVORITE", "type":"media", "path":"plugin://plugin.video.funimationnow/?action=player&video=Episode&barcode=7-7555878-59835-1481-1362-256", "thumbnail":"http://www.ggg.com"}, "id": 1}')

    logger.error(json.loads(lib))
    logger.error('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    logger.error('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')'''

    navigator.navigator().filtered(action, filtertype, params);

elif action == 'similarSeries':
    from resources.lib.indexers import navigator;

    navigator.navigator().filtered(action, filtertype, params);

elif action == 'videos':
    from resources.lib.indexers import navigator;

    navigator.navigator().filtered(action, filtertype, params);

elif action == 'updatemyqueue':
    from resources.lib.modules import control;
    from resources.lib.modules import utils;

    success = utils.addremovequeueitem(params);
    emessage = 'There was an error making your request.  Please try again.';

    if success is not None:

        emessage = success[1];

        if success[0] is True:
            control.refresh();

    utils.sendNotification(emessage, 10000);

elif action == 'updatewatched':
    from resources.lib.modules import control;
    from resources.lib.modules import utils;

    logger.error(params)

    success = utils.markwatchedstatus(params);

    if success is not None:
        control.refresh();


elif action == 'updatefavorites':
    from resources.lib.modules import utils;

    utils.updatefavorites(params);


elif action == 'player':
    from resources.lib.modules import utils;
    
    showinfo = utils.gathermeta(params);

    if showinfo is not None:
        from resources.lib.modules.player import player;

        player().run(showinfo);

    
elif action == 'searchNavigator':
    from resources.lib.modules import control;
    from resources.lib.modules import utils;

    search_text = utils.implementsearch();

    if search_text is not None:

        #url = self.search_link + urllib.quote_plus(q)
        url = '%s?action=search&search=%s' % (sys.argv[0], search_text);
        control.execute('Container.Update(%s)' % url);

elif action == 'search':
    from resources.lib.indexers import navigator;

    navigator.navigator().search(action, params);

elif action == 'loginNavigator':
    from resources.lib.modules import utils;

    utils.promptForLogin();
    utils.checkcookie();






    

'''
elif action == 'playItem':
    from resources.lib.sources import sources
    sources().playItem(title, source)
'''

    

    

'''
    elif action == 'movieNavigator':
        from resources.lib.indexers import navigator
        navigator.navigator().movies()

    elif action == 'movieliteNavigator':
        from resources.lib.indexers import navigator
        navigator.navigator().movies(lite=True)

    elif action == 'mymovieNavigator':
        from resources.lib.indexers import navigator
        navigator.navigator().mymovies()

    elif action == 'mymovieliteNavigator':
        from resources.lib.indexers import navigator
        navigator.navigator().mymovies(lite=True)

    elif action == 'tvNavigator':
        from resources.lib.indexers import navigator
        navigator.navigator().tvshows()

    elif action == 'tvliteNavigator':
        from resources.lib.indexers import navigator
        navigator.navigator().tvshows(lite=True)

    elif action == 'mytvNavigator':
        from resources.lib.indexers import navigator
        navigator.navigator().mytvshows()

    elif action == 'mytvliteNavigator':
        from resources.lib.indexers import navigator
        navigator.navigator().mytvshows(lite=True)

    elif action == 'downloadNavigator':
        from resources.lib.indexers import navigator
        navigator.navigator().downloads()

    elif action == 'toolNavigator':
        from resources.lib.indexers import navigator
        navigator.navigator().tools()

    elif action == 'searchNavigator':
        from resources.lib.indexers import navigator
        navigator.navigator().search()

    elif action == 'viewsNavigator':
        from resources.lib.indexers import navigator
        navigator.navigator().views()

    elif action == 'clearCache':
        from resources.lib.indexers import navigator
        navigator.navigator().clearCache()

    elif action == 'movies':
        from resources.lib.indexers import movies
        movies.movies().get(url)

    elif action == 'moviePage':
        from resources.lib.indexers import movies
        movies.movies().get(url)

    elif action == 'movieWidget':
        from resources.lib.indexers import movies
        movies.movies().widget()

    elif action == 'movieSearch':
        from resources.lib.indexers import movies
        movies.movies().search(query)

    elif action == 'moviePerson':
        from resources.lib.indexers import movies
        movies.movies().person(query)

    elif action == 'movieGenres':
        from resources.lib.indexers import movies
        movies.movies().genres()

    elif action == 'movieLanguages':
        from resources.lib.indexers import movies
        movies.movies().languages()

    elif action == 'movieCertificates':
        from resources.lib.indexers import movies
        movies.movies().certifications()

    elif action == 'movieYears':
        from resources.lib.indexers import movies
        movies.movies().years()

    elif action == 'moviePersons':
        from resources.lib.indexers import movies
        movies.movies().persons(url)

    elif action == 'movieUserlists':
        from resources.lib.indexers import movies
        movies.movies().userlists()

    elif action == 'channels':
        from resources.lib.indexers import channels
        channels.channels().get()

    elif action == 'tvshows':
        from resources.lib.indexers import tvshows
        tvshows.tvshows().get(url)

    elif action == 'tvshowPage':
        from resources.lib.indexers import tvshows
        tvshows.tvshows().get(url)

    elif action == 'tvSearch':
        from resources.lib.indexers import tvshows
        tvshows.tvshows().search(query)

    elif action == 'tvPerson':
        from resources.lib.indexers import tvshows
        tvshows.tvshows().person(query)

    elif action == 'tvGenres':
        from resources.lib.indexers import tvshows
        tvshows.tvshows().genres()

    elif action == 'tvNetworks':
        from resources.lib.indexers import tvshows
        tvshows.tvshows().networks()

    elif action == 'tvCertificates':
        from resources.lib.indexers import tvshows
        tvshows.tvshows().certifications()

    elif action == 'tvPersons':
        from resources.lib.indexers import tvshows
        tvshows.tvshows().persons(url)

    elif action == 'tvUserlists':
        from resources.lib.indexers import tvshows
        tvshows.tvshows().userlists()

    elif action == 'seasons':
        from resources.lib.indexers import episodes
        episodes.seasons().get(tvshowtitle, year, imdb, tvdb)

    elif action == 'episodes':
        from resources.lib.indexers import episodes
        episodes.episodes().get(tvshowtitle, year, imdb, tvdb, season, episode)

    elif action == 'calendar':
        from resources.lib.indexers import episodes
        episodes.episodes().calendar(url)

    elif action == 'tvWidget':
        from resources.lib.indexers import episodes
        episodes.episodes().widget()

    elif action == 'calendars':
        from resources.lib.indexers import episodes
        episodes.episodes().calendars()

    elif action == 'episodeUserlists':
        from resources.lib.indexers import episodes
        episodes.episodes().userlists()

    elif action == 'refresh':
        from resources.lib.modules import control
        control.refresh()

    elif action == 'queueItem':
        from resources.lib.modules imrt control
        control.queueItem()

    elif action == 'openSettings':
        from resources.lib.modules import control
        control.openSettings(query)

    elif action == 'artwork':
        from resources.lib.modules import control
        control.artwork()

    elif action == 'addView':
        from resources.lib.modules import views
        views.addView(content)

    elif action == 'moviePlaycount':
        from resources.lib.modules import playcount
        playcount.movies(imdb, query)

    elif action == 'episodePlaycount':
        from resources.lib.modules import playcount
        playcount.episodes(imdb, tvdb, season, episode, query)

    elif action == 'tvPlaycount':
        from resources.lib.modules import playcount
        playcount.tvshows(name, imdb, tvdb, season, query)

    elif action == 'trailer':
        from resources.lib.modules import trailer
        trailer.trailer().play(name, url)

    elif action == 'traktManager':
        from resources.lib.modules import trakt
        trakt.manager(name, imdb, tvdb, content)

    elif action == 'authTrakt':
        from resources.lib.modules import trakt
        trakt.authTrakt()

    elif action == 'rdAuthorize':
        from resources.lib.modules import debrid
        debrid.rdAuthorize()

    elif action == 'download':
        import json
        from resources.lib.sources import sources
        from resources.lib.modules import downloader
        try: downloader.download(name, image, sources().sourcesResolve(json.loads(source)[0], True))
        except: pass

    elif action == 'play':
        from resources.lib.sources import sources
        sources().play(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)

    elif action == 'addItem':
        from resources.lib.sources import sources
        sources().addItem(title)

    elif action == 'playItem':
        from resources.lib.sources import sources
        sources().playItem(title, source)

    elif action == 'alterSources':
        from resources.lib.sources import sources
        sources().alterSources(url, meta)

    elif action == 'clearSources':
        from resources.lib.sources import sources
        sources().clearSources()
'''

