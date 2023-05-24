import json


class _Card:
    def __init__(self, cardtype: str, value, name, color=None, action=None):
        self.type = cardtype
        self.value = value
        self.color = color
        self.name = name
        self.action = action


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


topcard = _Card(cardtype="number", value=3, color=["red", "blue", "green"], name="redbluetwo")

a = _Card(cardtype="number", value=1, color=["red"], name="redone")
b = _Card(cardtype="number", value=3, color=["red"], name="redthree")
c = _Card(cardtype="number", value=1, color=["blue"], name="redone")
d = _Card(cardtype="number", value=2, color=["green"], name="redone")
e = _Card(cardtype="number", value=1, color=["blue", "red"], name="redone")
f = _Card(cardtype="number", value=1, color=["green"], name="redone")
g = _Card(cardtype="number", value=3, color=["red"], name="redone")

playercards = [a, b, c, d, e, f, g]

checkCards(topcard, playercards)
