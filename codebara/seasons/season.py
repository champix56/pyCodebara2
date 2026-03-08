import json
import datetime
import dateutil.parser
def seasonsFilter(location='./seasons/seasons.json')->list[dict]:
    runningSeasons=[]
    with open(location, "r") as jsonfile:
        data = json.load(jsonfile)
        for season in data['seasons']:
             with open('.'+season['loc'], "r") as seasonjsonfile:
                dataSeason = json.load(seasonjsonfile)
                if dataSeason['endTime'] is None:
                    runningSeasons.append(dataSeason)
                else:
                    endTime = dateutil.parser.parse(dataSeason['endTime'])
                    now=datetime.datetime.utcnow()
                    if(endTime>now):
                        runningSeasons.append(dataSeason)
        # end for
        return runningSeasons
def seasonLoader(location="./season/season.json") -> dict:
    with open(location, "r") as jsonfile:
        data = json.load(jsonfile)
        return data
    