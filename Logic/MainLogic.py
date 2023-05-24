from Misc.User import User
from Misc.JSONObjects import *
from Socket import Connection


def main(game: Game):
    """ Main AI Logic
    """

    # currentPlayer = game.getCurrentPlayer()

    # Check if it's users turn
    # if user.sid == game.currentPlayer["socketId"]:

    player = game.getCurrentPlayer()

    # Check if user is disqualified
    while not player.disqualified:

        # player = game.getPlayer(user.sid)
        playerCards = player.getCards()
        topCard = game.getTopCard()
        print(topCard.name)

        print("objects complete")

        # When turn starts check for matching pairs - discard matches or take a card
        if game.state == "turn_start":
            cardMatches = checkCards(topCard, playerCards)
            print("cardmatches complete")

            # decide which cards are discarded
            if cardMatches:
                discardAction = discardCards(topCard, cardMatches)
                Connection.playAction(discardAction)

            else:
                takeAction = Action(type="take",
                                    explanation="no cards to discard")
                Connection.playAction(takeAction)

        # After drawing a card check for matches again - discard or say "nope"
        if game.state == "card_drawn":
            cardMatches = checkCards(topCard, playerCards)

            # decide which cards are discarded
            if cardMatches:
                discardAction = discardCards(topCard, cardMatches)
                Connection.playAction(discardAction)

            else:
                takeAction = Action(type="nope",
                                    explanation="no cards to discard")
                Connection.playAction(takeAction)


def discardCards(topCard, matchedColors) -> Action:
    key = min(matchedColors)
    discardCardsList = []
    for i in range(topCard.value):
        discardCardsList.append(matchedColors[key][i])
    discardAction = Action(type="discard",
                           explanation="random pick",
                           cards=discardCardsList)
    return discardAction


def checkCards(topCard: Card, playerCards: list) -> dict:
    # Save all matching cards to a dictionary
    matchedColors = {}
    for color in topCard.color:
        matchedCards = []
        for card in playerCards:
            for cardcolor in card.color:
                if color == cardcolor:
                    matchedCards.append(card)
        matchedColors[color] = matchedCards

    # Remove cards if they aren't enough to discard
    keysToRemove = []
    for key in matchedColors:
        if len(matchedColors[key]) < topCard.value:
            keysToRemove.append(key)

    for key in keysToRemove:
        del matchedColors[key]

    return matchedColors
