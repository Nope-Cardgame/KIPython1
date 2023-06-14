from Misc.JSONObjects import *
from Logic import MainLogic

topcard = Card(type="nominate", value=2, colors=["green"], name="green nominate")

# a = _Card(type="number", value=1, colors=["red"], name="redone")
# b = _Card(type="number", value=3, colors=["red"], name="redthree")
# c = _Card(type="reset", value=None, colors=["blue"], name="reset")
# d = _Card(type="number", value=2, colors=["green"], name="greentwo")
# e = _Card(type="number", value=1, colors=["blue", "red"], name="redblueone")
# f = _Card(type="number", value=1, colors=["green"], name="greenone")
# g = _Card(type="number", value=3, colors=["red"], name="redthree")
# h = _Card(type="invisible", value=None, colors=["red"], name="invisible")
# i = _Card(type="number", value=3, colors=["red"], name="redthree")
# j = _Card(type="number", value=3, colors=["red"], name="redthree")
# reset = _Card(type="reset", value=None, colors=['green', 'yellow', "blue", "red"], name="reset")
# nominatemulti = _Card(type="nominate", value=None, colors=['green', 'yellow', "blue", "red"], name="multi nominate")

# playercards = [a, b, reset, e, nominatemulti]
#
# p1 = _Player("p1", "12345", 5, [a, b, c])
# p2 = _Player("p2", "12345", 7, [a, b, c])
# p3 = _Player("p3", "12345", 2, [a, b, c])
# p4 = _Player("p4", "12345", 4, [a, b, c])
#
# playersList = [p1, p2, p3, p4]

discardPile = [{'type': 'nominate', 'colors': ['green'], 'name': 'green nominate'}]

# cards = [{'type': 'reset', 'colors': ['green', 'yellow', "blue", "red"], 'name': 'reset', 'value': 1},
#          {'type': 'number', 'colors': ['red', 'blue'], 'name': 'red and blue one', 'value': 1},
#          {'type': 'number', 'colors': ['blue', 'yellow'], 'name': 'blue and yellow two', 'value': 2},
#          {'type': 'number', 'colors': ['blue'], 'name': 'blue two', 'value': 2},
#          {'type': 'number', 'colors': ['yellow'], 'name': 'yellow one', 'value': 1},
#          {'type': 'nominate', 'colors': ['green', 'blue', "yellow", "red"], 'name': 'multi nominate', 'value': None},
#          {'type': 'number', 'colors': ['red', 'blue'], 'name': 'red and blue two', 'value': 2},
#          {'type': 'number', 'colors': ['red', 'yellow'], 'name': 'red and yellow one', 'value': 1}]
#
# matchcards = {"red": [a, b, e, g],
#               "blue": [c, e]}

# cardsList = []
# for cardData in cards:
#     card = _Card(**cardData)
#     cardsList.append(card)

player1 = {'username': 'deedz',
           'socketId': 'R7MzJTSb1LBHzWdXAAJT',
           'cardAmount': 8,
           'cards': [{'type': 'number', 'colors': ['red', 'green'], 'name': 'red and green one', 'value': 1},
                     {'type': 'number', 'colors': ['blue'], 'name': 'blue two', 'value': 2},
                     {'type': 'number', 'colors': ['green', 'yellow'], 'name': 'green and yellow two', 'value': 2},
                     {'type': 'number', 'colors': ['red', 'yellow'], 'name': 'red and yellow one', 'value': 1},
                     {'type': 'number', 'colors': ['green'], 'name': 'green two', 'value': 2},
                     {'type': 'number', 'colors': ['blue', 'yellow'], 'name': 'blue and yellow two', 'value': 2},
                     {'type': 'number', 'colors': ['green'], 'name': 'green two', 'value': 2},
                     {'type': 'number', 'colors': ['red', 'yellow'], 'name': 'red and yellow two', 'value': 2}],
           'disqualified': False}

player2 = {'username': 'Dennis',
           'socketId': 'R7MzJTSb1LBHzWdXAAJT',
           'cardAmount': 8,
           'cards': [{'type': 'number', 'colors': ['red', 'green'], 'name': 'red and green one', 'value': 1},
                     {'type': 'number', 'colors': ['blue'], 'name': 'blue two', 'value': 2},
                     {'type': 'number', 'colors': ['green', 'yellow'], 'name': 'green and yellow two', 'value': 2},
                     {'type': 'number', 'colors': ['red', 'yellow'], 'name': 'red and yellow one', 'value': 1},
                     {'type': 'number', 'colors': ['green'], 'name': 'green two', 'value': 2},
                     {'type': 'number', 'colors': ['blue', 'yellow'], 'name': 'blue and yellow two', 'value': 2},
                     {'type': 'number', 'colors': ['green'], 'name': 'green two', 'value': 2},
                     {'type': 'number', 'colors': ['red', 'yellow'], 'name': 'red and yellow two', 'value': 2}],
           'disqualified': False}

testgame = {"id": "23345",
            "state": "turn_start",
            "noActionCards": "True",
            "noWildCards": "True",
            "oneMoreStartCard": "True",
            "players": [player1, player2],
            "discardPile": discardPile,
            "currentPlayer": player1}

# t = {"id": "1234",
#      "mode": {"mode": "round-robin", "numberofRounds": "10"},
#      "participants": [player1],
#      "games": [testgame],
#      }


def plistmax(playerlist):
    list = []
    for p in playerlist:
        list.append(int(p.cardAmount))

    print(list)
    ma = max(list)

    for p in playerlist:
        if ma == p.cardAmount:
            print(p.username)



game = Game(**testgame)

MainLogic.main(game)

