import json
import Fetcher
import Inspector
import os
import time

Goroth_dps_rank_var = {
    "encounterId": 2032,
    "metric": "dps",
    "difficulty": 5,
    "partition": 2,
    "page": 1
}

DH_rank_var = {
    "class": 12,
    "spec": 1,
}

DH_ability_crit = {
    "Chaos Strike": 0,
    "Annihilation": 0
}

Goroth_DH_dps_rank_var = Goroth_dps_rank_var.copy()
Goroth_DH_dps_rank_var.update(DH_rank_var)

target_dir = "data/"+time.strftime("%Y.%d.%m")
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

with open(target_dir+"/ranking.txt", "w") as rankingFile:
    rankingFile.write("report_id,fight_id,player_id,fight_start,fight_end,chaos_strike,annihilation,agility,mastery,critical,haste,ver,with_eoc\n")
    count = 0
    page = 0
    while count < 200:
        page+=1
        Goroth_DH_dps_rank_var["page"] = page
        rankings = Fetcher.fetch_ranking(Goroth_DH_dps_rank_var)["rankings"]
        for dh in rankings:
            if Inspector.is_auto_trans(dh):
                #Fetch fight data
                reportID = dh["reportID"]
                fightID = dh["fightID"]
                playerName = dh["name"]
                fights, friendlies = Fetcher.fetch_fights(reportID)
                fight, player = Inspector.extract_player_fight(fights, friendlies, fightID, playerName)

                #Take parameters in the fight data
                fight_start = fight["start_time"]
                fight_end = fight["end_time"]
                player_id = player["id"]

                #Fetch player's stats
                events = Fetcher.fetch_events(reportID,  fight_start, fight_end, player_id)
                player_stats = Inspector.extract_player_stats(events)

                if not player_stats == None:
                    #Fetch Chaos Strike and Annihilation's actual critical
                    damages = Fetcher.fetch_table(reportID, "damage-done", fight_start, fight_end, player_id)
                    ability_crit = Inspector.extract_actual_criti(damages, DH_ability_crit)

                    #Generate output
                    outputline = reportID+",%d,%d,%d,%d,%f,%f,%d,%d,%d,%d,%d,%d\n" % \
                                          (fightID, player_id, fight_start, fight_end,
                                           ability_crit["Chaos Strike"], ability_crit["Annihilation"],
                                           player_stats["agility"], player_stats["mastery"], player_stats["critical"],
                                           player_stats["haste"], player_stats["ver"], player_stats["with_eoc"])

                    print outputline
                    rankingFile.write(outputline)
