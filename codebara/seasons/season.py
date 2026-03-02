import json
def seasonLoader(location="./season/season.json") -> dict:
    with open(location, "r") as jsonfile:
        data = json.load(jsonfile)
        return data
    