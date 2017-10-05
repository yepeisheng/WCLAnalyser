import json

with open("const/classes.json", "r") as classfile:
    classes = json.load(classfile)
    print classes[0]