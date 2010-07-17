# -*- coding: UTF-8 -*-
from mochi import __MOCHI_FEED, __MOCHI_FEED_FORMAT_SUFFIX, Game, check_mochi_zip, get_game
from os.path import basename
from shutil import copyfileobj
from urlparse import urlsplit
from zipfile import ZipFile
import sys

if sys.version_info < (2, 6):
    import simplejson as json
else:
    import json

import os
import urllib2


def __url2name(url):
    return basename(urlsplit(url)[2])

def __download(url, store_location= None, local_filename = None ):
    try:
        local_name = __url2name(url)
        req = urllib2.Request(url)
        r = urllib2.urlopen(req)
        if r.info().has_key('Content-Disposition'):
            # If the response has Content-Disposition, we take file name from it
            local_name = r.info()['Content-Disposition'].split('filename=')[1]
            if local_name[0] == '"' or local_name[0] == "'":
                local_name = local_name[1:-1]
        elif r.url != url: 
            # if we were redirected, the real file name we take from the final URL
            local_name = __url2name(r.url)
        if local_filename: 
            # we can force to save the file as specified name
            local_name = local_filename
            
        if store_location:
            local_name = store_location + local_name 
        f = open(local_name, 'wb')
        copyfileobj(r, f)
        f.close()
        return True
    except:
        return False

            
def fetch_game(publisher_id, game_tag, filestore):
    """
    Fetches a game zip from mochiads and extracts its content to disk
    
    @type publisher_id: string
    @param publisher_id: Your mochiads Publisherid  
    
    @type game_tag: string
    @param game_tag: the game_tag of the game to fetch
    
    @type filestore: string
    @param filestore: A directory to extract the game content 
    """
    full_url = __MOCHI_FEED + publisher_id + '/'+game_tag + __MOCHI_FEED_FORMAT_SUFFIX
    response = urllib2.urlopen(full_url)
    game_info =json.load(response)
    game = Game(game_info['games'][0]) 
    downloaded = __download(game.zip_url, store_location = filestore)
    if not downloaded:
        return None
    zipfile_name = filestore + game.get_zip_filename()
    game_zip = ZipFile(zipfile_name)
    if not check_mochi_zip(game_zip, game):
        game_zip.close()
        os.remove(zipfile_name)
        return None
    
    if sys.version_info < (2, 6):
        __extract_zip(game_zip, filestore)
    else:
        game_zip.extractall(filestore)

    game_zip.close()
    os.remove(zipfile_name)
    return get_game(filestore, slug=game.slug)


def __extract_zip(zipfile, dir):
    _makedirs(zipfile, dir)
    for i, name in enumerate(zipfile.namelist()):
        if not name.endswith('/'):
            outfile = open(os.path.join(dir, name), 'wb')
            outfile.write(zipfile.read(name))
            outfile.flush()
            outfile.close()

def _makedirs(zipfile, dir):
    for i, name in enumerate(zipfile.namelist()):
        upperdirs = os.path.dirname(os.path.join(dir, name))
        if upperdirs and not os.path.exists(upperdirs):
            os.makedirs(upperdirs)
