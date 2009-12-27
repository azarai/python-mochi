# -*- coding: UTF-8 -*-
import os, glob
from stat import *
import sys, re
if sys.version_info < (2, 6):
    import simplejson as json
else:
    import json

MOCHI_FEED = 'http://www.mochimedia.com/feeds/games/'
MOCHI_FEED_FORMAT_SUFFIX = '/?format=json;'
MOCHI_URL_PREFIX = 'http://.*\.mochiads\.com/c/g/'

class Game():
    """
    A mochi game
    """
    def __init__(self, data):
        """
        Creates game instace from a mochi json object
        
        @type data: dict of a mochi game json
        @param data: mochi game data
        """
        self.data = data
  
    def get_swf_name(self):
        """
        Gets the filename of the swf
        
        @rtype: string
        @return: filename of the swf
        """
        return re.sub(MOCHI_URL_PREFIX, "", self.swf_url)
   
    def get_thumb_url(self):
        """
        Gets the url part of the game thumbnail without the mochi servers
        
        @rtype: string
        @return: url of the thumbnail
        """
        return re.sub(MOCHI_URL_PREFIX, "", self.thumbnail_url)

    def get_zip_filename(self):
        """
        Gets the filename of the game zipfile
        
        @rtype: string
        @return: filename of the game zipfile
        """
        return re.sub(MOCHI_URL_PREFIX, "", self.zip_url)
   
    def __getattr__(self, name):
        if self.data.has_key(name):
            return self.data[name]
        raise AttributeError, '%s does not exist on %s' % (name, self.__unicode__())
    
    def __getstate__(self):
        return self.data
    
    def __setstate__(self, state):
        self.data = state
    
    def __unicode__(self):
        return self.slug

def check_mochi_zip(game_zip, game):
    """
    Checks if the given zipfile is really the mochi game zipfile for the given game
    
    @type game_zip: ZipFile
    @param game_zip: A ZipFile of a mochi game
    
    @type game: Game
    @param game: The Game that should belong to game_zip
    
    @rtype: boolean
    @return: False if theres any file inside the zip thats not part of the given game
    """
    has_metadata = False
    has_swf = False

    for zip_info in game_zip.infolist():
        if not zip_info.filename.startswith(game.slug):
            return False
        if zip_info.filename == game.slug +"/" + '__metadata__.json':
            has_metadata = True
        if zip_info.filename == game.get_swf_name():
            has_swf = True
            
    if has_metadata and has_swf:
        return True
    return False

def list_games(filestore):
    games = []
    for file in os.listdir(filestore):
        pathname = os.path.join(filestore, file)
        mode = os.stat(pathname)[ST_MODE]
        if S_ISDIR(mode):
            metafile = os.path.join(pathname, '__metadata__.json')
            if os.path.exists(metafile):
                import codecs
                f = codecs.open( metafile, "r", "utf-8" )
                text = f.read()
                game = Game(json.loads(text))
                game.local_last_modifified = os.path.getmtime(metafile)
                games.append(game)
                f.close()
    return games

def get_game(filestore, game_tag=None, slug=None):
    if not game_tag and not slug:
        return None 
    games = list_games(filestore)
    for game in games:
        if game.game_tag == game_tag or game.slug == slug:
            return game