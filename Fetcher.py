import json
import requests

try:
    json_data_file = open("conf/application.conf")
    data = json.load(json_data_file)
    apikey = data["api_key"]
    json_data_file.close()
    
except:
    print "Your configuration file is wrong"

api_zones = "https://www.warcraftlogs.com:443/v1/zones?api_key="+apikey
api_class = "https://www.warcraftlogs.com:443/v1/classes?api_key="+apikey

with open("const/zones.json", "w") as zonefile:
    zones = requests.get(api_zones).json()
    json.dump(zones, zonefile, indent=4)

with open("const/classes.json", "w") as classfile:
    classes = requests.get(api_class).json()
    json.dump(classes, classfile, indent=4)
