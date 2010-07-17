# -*- coding: UTF-8 -*-
"""
Python-Mochi is a lib for working with the U{mochiads api <https://www.mochimedia.com/support/pub_docs>}
"""
import os, glob
from stat import *
import sys, re
if sys.version_info < (2, 6):
    import simplejson as json
else:
    import json

__MOCHI_FEED = 'http://www.mochimedia.com/feeds/games/'
__MOCHI_FEED_FORMAT_SUFFIX = '/?format=json;'
MOCHI_URL_PREFIX = 'http://.*\.mochiads\.com/c/g/'

class Game():
    """
    A single mochiads game
    """
    def __init__(self, data):
        """
        Creates game instace from a mochiads json object
        
        @type data: dict of a mochiads game json
        @param data: mochiads game data
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
        Gets the url part of the game thumbnail without the mochiads servers
        
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
    Checks if the given zipfile is really the mochiads game zipfile for the given game
    
    @type game_zip: C{zipfile.ZipFile}
    @param game_zip: A ZipFile of a mochiads game
    
    @type game: L{Game}
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
    """
    Lists all Games in the filestore
    
    @type filestore: path
    @param filestore: path to the dir where the games are stored
       
    @rtype: list of L{Game}
    @return: a list of all valid games found
    """
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
    """
    Get a game from the filestore by tag or slug
    
    @type filestore: path
    @param filestore: path to the dir where the games are stored

    @type game_tag: game_tag
    @param game_tag: path to the dir where the games are stored

    @type slug: slug
    @param slug: path to the dir where the games are stored
       
    @rtype: L{Game}
    @return: the game or None if not found
    """
    if not game_tag and not slug:
        return None 
    games = list_games(filestore)
    for game in games:
        if ( hasattr(game, 'game_tag') and game.game_tag == game_tag) or game.slug == slug:
            return game