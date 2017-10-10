import json
import Fetcher
import Inspector


Goroth_dps_rank_var = {
    "encounterId": 2032,
    "metric": "dps",
    "difficulty": 5,
    "partition": 2,
    "limit": 1,
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

rankings = Fetcher.fetch_ranking(Goroth_DH_dps_rank_var)["rankings"]

for dh in rankings:
    reportID = dh["reportID"]
    fightID = dh["fightID"]
    playerName = dh["name"]

    with open("test/fight.json", "w") as fightFile:
        json.dump(dh, fightFile, indent=4)

    fights, friendlies = Fetcher.fetch_fights(reportID)
    fight, player = Inspector.extract_player_fight(fights, friendlies, fightID, playerName)
    events = Fetcher.fetch_events(reportID,  fight["start_time"], fight["end_time"], player["id"])
    with open("test/events.json", "w") as eventfile:
        json.dump(events, eventfile, indent=4)

    palyer_stats = Inspector.extract_player_stats(events)
    with open("test/stats.json", "w") as statsFile:
        json.dump(palyer_stats, statsFile, indent=4)

    damages = Fetcher.fetch_table(reportID, "damage-done", fight["start_time"], fight["end_time"], player["id"])
    with open("test/damages.json", "w") as damagesFile:
        json.dump(damages, damagesFile, indent=4)

    ability_crit = Inspector.extract_actual_criti(damages, DH_ability_crit)
    with open("test/ability.json", "w") as abilityFile:
        json.dump(ability_crit, abilityFile, indent=4)


