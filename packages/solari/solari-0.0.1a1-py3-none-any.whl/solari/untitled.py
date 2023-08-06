import pymongo

client = pymongo.MongoClient()
db = client.game_ps_11

mongoTable = db["gameEuw"]

from match_stats import MatchStats
from stats.champions_rate_stats import ChampionPickrate, ChampionWinrate, ChampionBanrate, ChampionPresenceRate

ms = MatchStats(
    [
        ChampionPickrate(), 
        ChampionWinrate(), 
        ChampionBanrate(), 
        ChampionPresenceRate()
    ]
)

for g in mongoTable.find({ "gameDuration": { "$gt": 900 }, "mapId":11 }).limit(2000):
    ms.push_match(g)
    
ms.get_stats()