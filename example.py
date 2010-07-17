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