import json


class _Card:
    def __init__(self, type: str, value, name, colors=None, action=None):
        self.type = type
        self.value = value
        self.colors = colors
        self.name = name
        self.action = action


class _Player:

    def __init__(self, username, socketId, cardAmount, cards):
        self.username = username
        self.socketId = socketId
        self.cardAmount = cardAmount
        self.cards = cards


class _Tournament:

    def __init__(self,
                 id: str,
                 mode: dict,
                 participants: list[dict],
                 games: list[dict],
                 startTime: str = None,
                 endTime: str = None):
        self.id = id
        self.mode = mode
        self.participants = participants
        self.games = games
        self.startTime = startTime
        self.endTime = endTime


def checkCards(topCard: _Card, playerCards: list):
    matchedColors = {}
    for color in topCard.color:

        matchedCards = []
        for card in playerCards:
            for cardcolor in card.color:
                if color == cardcolor:
                    matchedCards.append(card)

        matchedColors[color] = matchedCards

    print(matchedColors)
    print(len(matchedColors["red"]))

    keysToRemove = []
    for key in matchedColors:
        if len(matchedColors[key]) < topCard.value:
            keysToRemove.append(key)

    for key in keysToRemove:
        del matchedColors[key]

    print(matchedColors)

    # decide which cards to discard
    if matchedColors:

        key = min(matchedColors)
        discardCards = []
        for i in range(topCard.value):
            discardCards.append(matchedColors[key][i])

        print(discardCards)

topcard = _Card(type="nominate", value=2, colors=["green"], name="green nominate")

a = _Card(type="number", value=1, colors=["red"], name="redone")
b = _Card(type="number", value=3, colors=["red"], name="redthree")
c = _Card(type="reset", value=None, colors=["blue"], name="reset")
d = _Card(type="number", value=2, colors=["green"], name="greentwo")
e = _Card(type="number", value=1, colors=["blue", "red"], name="redblueone")
f = _Card(type="number", value=1, colors=["green"], name="greenone")
g = _Card(type="number", value=3, colors=["red"], name="redthree")
h = _Card(type="invisible", value=None, colors=["red"], name="invisible")
i = _Card(type="number", value=3, colors=["red"], name="redthree")
j = _Card(type="number", value=3, colors=["red"], name="redthree")
reset = _Card(type="reset", value=None, colors=['green', 'yellow', "blue", "red"], name="reset")
nominatemulti = _Card(type="nominate", value=None, colors=['green', 'yellow', "blue", "red"], name="multi nominate")

playercards = [a,b,reset,e,nominatemulti]

p1 = _Player("p1", "12345", 5, [a,b,c])
p2 = _Player("p2", "12345", 7, [a,b,c])
p3 = _Player("p3", "12345", 2, [a,b,c])
p4 = _Player("p4", "12345", 4, [a,b,c])

playersList = [p1,p2,p3,p4]

discardPile = [topcard, c, a, d]

cards = [{'type': 'reset', 'colors': ['green', 'yellow', "blue", "red"], 'name': 'reset', 'value': 1},
         {'type': 'number', 'colors': ['red', 'blue'], 'name': 'red and blue one', 'value': 1},
         {'type': 'number', 'colors': ['blue', 'yellow'], 'name': 'blue and yellow two', 'value': 2},
         {'type': 'number', 'colors': ['blue'], 'name': 'blue two', 'value': 2},
         {'type': 'number', 'colors': ['yellow'], 'name': 'yellow one', 'value': 1},
         {'type': 'nominate', 'colors': ['green', 'blue', "yellow", "red"], 'name': 'multi nominate', 'value': None},
         {'type': 'number', 'colors': ['red', 'blue'], 'name': 'red and blue two', 'value': 2},
         {'type': 'number', 'colors': ['red', 'yellow'], 'name': 'red and yellow one', 'value': 1}]

matchcards = {"red": [a, b, e, g],
              "blue": [c, e]}

cardsList = []
for cardData in cards:
    card = _Card(**cardData)
    cardsList.append(card)

currentPlayer = {"username": "name",
                 "socketId": "1234dgf",
                 "cardAmount": 6,
                 "cards": [{'type': 'number', 'colors': ['green'], 'name': 'green two', 'value': 2},
                           {'type': 'number', 'colors': ['blue', 'yellow'], 'name': 'blue and yellow three',
                            'value': 3},
                           {'type': 'number', 'colors': ['green', 'yellow'], 'name': 'green and yellow three',
                            'value': 3}, {'type': 'number', 'colors': ['green'], 'name': 'green one', 'value': 1},
                           {'type': 'number', 'colors': ['yellow'], 'name': 'yellow two', 'value': 2},
                           {'type': 'reset', 'colors': ['green', 'blue'], 'name': 'green and blue three', 'value': 3},
                           {'type': 'number', 'colors': ['red', 'yellow'], 'name': 'red and yellow one', 'value': 1},
                           {'type': 'number', 'colors': ['red', 'green'], 'name': 'red and green one', 'value': 1}]}

game = {"id": "23345",
        "state": "game_turn",
        "noActionCards": "True",
        "noWildCards": "True",
        "oneMoreStartCard": "True",
        "players": [currentPlayer]}

t = {"id": "1234",
     "mode": {"mode": "round-robin", "numberofRounds": "10"},
     "participants": [currentPlayer],
     "games": [game],
     }

def plistmax(playerlist):

    list = []
    for p in playerlist:
        list.append(int(p.cardAmount))

    print(list)
    ma = max(list)

    for p in playerlist:
        if ma == p.cardAmount:
            print(p.username)


def matchCardsByColor(topCard, playerCards) :
    """ Check the players cards for completed sets, depending on the top card

    :param topCard: The current top card
    :param playerCards: The current players cards
    :return: Dictionary of matching cards which complete a required set - with colors as keys and a list of cards as value
    """

    # Save all matching cards to a dictionary
    matchedColors = {}
    for color in topCard.colors:
        matchedCards = []
        for card in playerCards:
            for cardcolor in card.colors:
                if color == cardcolor:
                    matchedCards.append(card)
        matchedColors[color] = matchedCards

    # Remove cards if they aren't enough to discard
    keysToRemove = []
    for key in matchedColors:
        if len(matchedColors[key]) < int(topCard.value):
            keysToRemove.append(key)

    for key in keysToRemove:
        del matchedColors[key]

    return matchedColors

def testforactioncards(matchedCards):
    actionCardsList = []

    for color in matchedCards:
        for card in matchedCards[color]:
            if not card.type == "number":
                actionCardsList.append(card)
    print(actionCardsList)

    uniqueActionCards = []

    for card in actionCardsList:
        if card in uniqueActionCards:
            pass
        else:
            uniqueActionCards.append(card)

    return uniqueActionCards


def playActionCard(actionCardsOnHand):
    if len(actionCardsOnHand) > 1:
        print("choose actioncard")
    else:
        if actionCardsOnHand[0].type == "nominate":
            print("nominate")
        else:
            discardSingleCard(actionCardsOnHand[0])


def discardSingleCard(card):

    parsedCard = [vars(card)]
    print(parsedCard)
    return parsedCard

def checkTopCardForActionCards(discardPileList, index):

    topCard = discardPileList[index]

    match topCard.type:
        case "invisible":
            for card in range(index, len(discardPile)):
                index += 1
                topCard = checkTopCardForActionCards(discardPileList, index)
                return topCard

        case "reset":
            topCard.value = 1
            topCard.colors = ["red", "green", "blue", "yellow"]
            topCard.name = "resetfound"
            return topCard

        case "number":
            return topCard


matchedcards = matchCardsByColor(topcard, playercards)
actioncardsmatch = testforactioncards(matchedcards)
print(str(actioncardsmatch))

