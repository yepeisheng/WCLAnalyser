import json
import requests
import os

try:
    json_data_file = open("conf/application.conf")
    data = json.load(json_data_file)
    apikey = data["api_key"]
    json_data_file.close()
    
except:
    print "Your configuration file is wrong"


def fetch_zones():
    print "Fetching zone data from Warcraftlog"
    api_zones = "https://www.warcraftlogs.com:443/v1/zones?api_key="+apikey
    with open("const/zones.json", "w") as zonefile:
        zones = requests.get(api_zones).json()
        json.dump(zones, zonefile, indent=4)


def fetch_classes():
    print "Fetching class data from Warcraftlog"
    api_class = "https://www.warcraftlogs.com:443/v1/classes?api_key="+apikey
    with open("const/classes.json", "w") as classfile:
        classes = requests.get(api_class).json()
        json.dump(classes, classfile, indent=4)


def load_zones(force = False):
    if not os.path.exists("const/zones.json") or force:
        fetch_zones()

    with open("const/zones.json", "r") as classfile:
        classes = json.load(classfile)
    return classes


def load_classes(force = False):
    if not os.path.exists("const/classes.json") or force:
        fetch_classes()

    with open("const/classes.json", "r") as classfile:
        classes = json.load(classfile)
    return classes


def fetch_ranking(rank_var = {"encounterId": 2032,
                              "metric": "dps",
                              "difficulty": 5,
                              "partition": 1,
                              "class": 12,
                              "spec": 1,
                              "limit": 1,
                              "page": 1}):
    print "Fetching ranking"
    rank_var["api_key"] = apikey
    api_rank = "https://www.warcraftlogs.com:443/v1/rankings/encounter/"+str(rank_var["encounterId"])
    rank = requests.get(api_rank, rank_var).json()
    return rank


def fetch_fights(reportID):
    api_fights = "https://www.warcraftlogs.com:443/v1/report/fights/"+reportID+"?api_key="+apikey
    fights = requests.get(api_fights).json()
    friendlies = fights["friendlies"]
    fights = fights["fights"]
    return fights, friendlies


def fetch_events(reportID, start, end, playerId):
    api_events = "https://www.warcraftlogs.com:443/v1/report/events/"+reportID
    events_var =  {"start": start,
                   "end": end,
                   "actorid": playerId,
                   "api_key": apikey}
    events = requests.get(api_events, events_var).json()
    return events["events"]


def fetch_table(reportID, view, start, end, playerID):
    api_table = "https://www.warcraftlogs.com:443/v1/report/tables/"+view+"/"+reportID
    table_var = {
        "api_key": apikey,
        "start": start,
        "end": end,
        "sourceid": playerID
    }
    table = requests.get(api_table, table_var).json()
    return table["entries"]
