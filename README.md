Python-Mochi is a lib for working with the [mochi api](https://www.mochimedia.com/support/pub_docs "link to mochi") in python.

### What it currently does

  - fetch game by gametag from mochiads server
  - unzip and store game locally
  - list games in local filestore
  - get game by slug or game_tag from local filestore

### Code:

[Download python-mochi from git repository](http://github.com/azarai/python-mochi "python mochi repro")  
Tested with python 2.5 and 2.6

### License:
BSD

### Short example:

    :::python
    from mochi import list_games
    from mochi.autopost import fetch_game
    
    PUBLISHER_ID = 'your publisher id'
    
    game_tag= '18c4fc4b1b391f11'
    
    filestore = '.'
    
    game = fetch_game(PUBLISHER_ID, game_tag, filestore)
    print 'downloaded game %s ' % game.slug
    
    games = list_games(filestore)
    
    for game in games:
        print game.slug