import json


class _Card:
    def __init__(self, type: str, value, name, colors=None, action=None):
        self.type = type
        self.value = value
        self.color = colors
        self.name = name
        self.action = action


class _Player:

    def __init__(self, username, socketId, cardAmount, cards):
        self.username = username
        self.socketId = socketId
        self.cardAmount = cardAmount
        self.cards = cards


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


# topcard = _Card(cardtype="number", value=3, color=["red", "blue", "green"], name="redbluetwo")

# a = _Card(cardtype="number", value=1, color=["red"], name="redone")
# b = _Card(cardtype="number", value=3, color=["red"], name="redthree")
# c = _Card(cardtype="number", value=1, color=["blue"], name="redone")
# d = _Card(cardtype="number", value=2, color=["green"], name="redone")
# e = _Card(cardtype="number", value=1, color=["blue", "red"], name="redone")
# f = _Card(cardtype="number", value=1, color=["green"], name="redone")
# g = _Card(cardtype="number", value=3, color=["red"], name="redone")

# playercards = [a, b, c, d, e, f, g]

# checkCards(topcard, playercards)

cards = {'cards': [{'type': 'number', 'colors': ['green', 'yellow'], 'name': 'green and yellow one', 'value': 1},
                   {'type': 'number', 'colors': ['red', 'blue'], 'name': 'red and blue one', 'value': 1},
                   {'type': 'number', 'colors': ['green', 'yellow'], 'name': 'green and yellow two', 'value': 2},
                   {'type': 'number', 'colors': ['blue'], 'name': 'blue two', 'value': 2},
                   {'type': 'number', 'colors': ['yellow'], 'name': 'yellow one', 'value': 1},
                   {'type': 'number', 'colors': ['green', 'blue'], 'name': 'green and blue two', 'value': 2},
                   {'type': 'number', 'colors': ['green', 'blue'], 'name': 'green and blue two', 'value': 2},
                   {'type': 'number', 'colors': ['green', 'yellow'], 'name': 'green and yellow one', 'value': 1}]}

# cardsList = []
# for cardData in cards["cards"]:
#     card = _Card(*cardData)
#     cardsList.append(card)
#
# print(cardsList)

currentPlayer = {"username": "name",
                 "socketId": "1234dgf",
                 "cardAmount": 6,
                 "cards": [{'type': 'number', 'colors': ['green'], 'name': 'green two', 'value': 2}, {'type': 'number', 'colors': ['blue', 'yellow'], 'name': 'blue and yellow three', 'value': 3}, {'type': 'number', 'colors': ['green', 'yellow'], 'name': 'green and yellow three', 'value': 3}, {'type': 'number', 'colors': ['green'], 'name': 'green one', 'value': 1}, {'type': 'number', 'colors': ['yellow'], 'name': 'yellow two', 'value': 2}, {'type': 'number', 'colors': ['green', 'blue'], 'name': 'green and blue three', 'value': 3}, {'type': 'number', 'colors': ['red', 'yellow'], 'name': 'red and yellow one', 'value': 1}, {'type': 'number', 'colors': ['red', 'green'], 'name': 'red and green one', 'value': 1}]}


discardPile = [{'colors': ['red', 'green'], 'name': 'red and green two', 'type': 'number', 'value': 2}]

# topcard = _Card(**discardPile[0])
# print(topcard.color)

cardsList = []
for cardData in currentPlayer["cards"]:
    card = _Card(**cardData)
    print(card.color)
    cardsList.append(card)


