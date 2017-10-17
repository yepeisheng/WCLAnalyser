import json


def extract_fight(fights, fightID):
    for fight in fights:
        if fight["id"] == fightID:
            return fight
    return None


def extract_player(friendlies, playerName):
    for player in friendlies:
        if player["name"] == playerName:
            return player
    return None


def extract_player_fight(fights, friendlies, fightID, playerName):
    fight = extract_fight(fights, fightID)
    player = extract_player(friendlies, playerName)
    return fight, player


def is_auto_trans(dh):
    felblade = False
    demon_blades = False
    chaos_blades = False
    for talent in dh["talents"]:
        if talent["name"] == "Felblade":
            felblade = True
        if talent["name"] == "Demon Blades":
            demon_blades = True
        if talent["name"] == "Chaos Blades":
            chaos_blades = True
    return felblade and demon_blades and chaos_blades


def use_eye_command(dh):
    for gear in dh["gear"]:
        if gear["name"] == "Eye of Command":
            return True
    return False


def extract_eyeofcommand(statsEvent):
    with open("const/eyeofcommand.json", "r") as eoc_file:
        eoc = json.load(eoc_file)
    for gear in statsEvent["gear"]:
        if gear["id"] == eoc["item_id"]:
            return eoc["base_buff"][str(gear["itemLevel"])]*10
    return 0


def extract_player_stats(events):
    base_stats = None
    for event in events:
        if event["type"] == "combatantinfo":
            eyeofcommand_basis = extract_eyeofcommand(event)
            base_stats = {
                "agility": event["agility"],
                "mastery": event["mastery"],
                "critical": event["critMelee"] + eyeofcommand_basis,
                "haste": event["hasteMelee"],
                "ver": event["versatilityDamageDone"],
                "with_eoc": eyeofcommand_basis != 0
            }
    return base_stats


def extract_actual_criti(table_entries, ability_names):
    result = ability_names.copy()
    for entry in table_entries:
        if entry["name"] in result:
            result[entry["name"]] = (1.0 * entry["critHitCount"])/entry["hitCount"]
    return result
