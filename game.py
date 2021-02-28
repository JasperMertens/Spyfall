from common import loadConfig

import random

class Player:
    def __init__ (self, fullName, shortName = ""):
        self.fullName = fullName
        self.shortName = fullName if shortName == "" else shortName
        self.isSpy = False
        self.score = 0

def createPlayers ():
    fullNamesRaw = loadConfig()['Game']['player names'].split(',')
    fullNames = [fn.strip() for fn in fullNamesRaw]
    return [Player(fullName=fn,
                   shortName=fn.split()[0]) for fn in fullNames]

def getLocations ():
    locationsRaw = loadConfig()['Game']['locations'].split(',')
    return [l.strip() for l in locationsRaw]

def selectRandomLocation (locations):
    return random.choice(locations)

def selectRandomSpies (numberOfSpies, players):
    result = []
    for _ in range(numberOfSpies):
        result.append(random.choice([p for p in players if p not in result]))
    return result
    
def informPlayers (location, spies, roundNumber, players, chatter, debug=False):
    roundMsg = "Starting round {}\n".format(roundNumber)
    for player in players:
        spyMsg = roundMsg + "You are a spy, {}!".format(player.shortName)
        locationMsg = roundMsg + "The location is '{}', {}".format(location, player.shortName)

        if (player in spies):
            chatter.sendMessage(spyMsg, player.fullName)

        else:
            chatter.sendMessage(locationMsg, player.fullName)

class Game:
    def __init__ (self, chatter):
        self.players = createPlayers()
        self.chatter = chatter
        self.roundNumber = 0

    def setupNewRound (self):
        self.roundNumber += 1
        locations = getLocations()
        location = selectRandomLocation(locations)
        spy = selectRandomSpies(1, self.players)
        informPlayers(location, spy, self.roundNumber,
                      self.players, self.chatter)

