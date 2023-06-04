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

topcard = _Card(type="number", value=3, colors=["red", "blue"], name="redbluetwo")

a = _Card(type="number", value=1, colors=["red"], name="redone")
b = _Card(type="number", value=3, colors=["red"], name="redthree")
c = _Card(type="reset", value=1, colors=["blue"], name="redone")
d = _Card(type="number", value=2, colors=["green"], name="redone")
e = _Card(type="number", value=1, colors=["blue", "red"], name="redone")
f = _Card(type="number", value=1, colors=["green"], name="redone")
g = _Card(type="number", value=3, colors=["red"], name="redone")

p1 = _Player("p1", "12345", 5, [a,b,c])
p2 = _Player("p2", "12345", 7, [a,b,c])
p3 = _Player("p3", "12345", 2, [a,b,c])
p4 = _Player("p4", "12345", 4, [a,b,c])

playersList = [p1,p2,p3,p4]

# playercards = [a, b, c, d, e, f, g]

# checkCards(topcard, playercards)

cards = [{'type': 'reset', 'colors': ['green', 'yellow'], 'name': 'green and yellow one', 'value': 1},
         {'type': 'number', 'colors': ['red', 'blue'], 'name': 'red and blue one', 'value': 1},
         {'type': 'number', 'colors': ['green', 'yellow'], 'name': 'green and yellow two', 'value': 2},
         {'type': 'number', 'colors': ['blue'], 'name': 'blue two', 'value': 2},
         {'type': 'number', 'colors': ['yellow'], 'name': 'yellow one', 'value': 1},
         {'type': 'number', 'colors': ['green', 'blue'], 'name': 'green and blue two', 'value': 2},
         {'type': 'number', 'colors': ['green', 'blue'], 'name': 'green and blue two', 'value': 2},
         {'type': 'number', 'colors': ['green', 'yellow'], 'name': 'green and yellow one', 'value': 1}]

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

discardPile = [{'colors': ['red', 'green'], 'name': 'red and green two', 'type': 'number', 'value': 2}]

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

def test(matchedCards):
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


# l = test(matchcards)
# playActionCard(l)

# plistmax(playersList)


amount = 2//3
print(amount)
