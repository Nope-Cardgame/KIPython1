from Misc.JSONObjects import *
from Socket import Connection


def main(game: Game):
    """ Main AI Logic
    """

    player = game.getCurrentPlayer()

    # Check if user is disqualified
    if not player.disqualified:
        playerCards = player.getCards()
        topCard = game.getTopCard()

        cardMatches = matchCardsByColor(topCard, playerCards)
        actionCardsOnHand = checkForActionCards(cardMatches)

        # When turn starts check for matching pairs - discard matches or take a card
        makeMove(actionCardsOnHand, cardMatches, topCard, game)


def makeMove(actionCardsOnHand, cardMatches, topCard, game):
    # decide which cards are discarded
    if cardMatches:
        if actionCardsOnHand:
            playActionCard(actionCardsOnHand, game)
        else:
            discardAction = discardCardSet(topCard, cardMatches)
            Connection.playAction(discardAction)

    else:
        match game.state:
            case "turn_start":
                specifyActionType("draw")
            case "card_drawn":
                specifyActionType("nope")


def playActionCard(actionCardsOnHand: list, game: Game):
    """

    :param actionCardsOnHand:
    :return:
    """

    if len(actionCardsOnHand) > 1:

        order = ["nominate", "invisible", "reset"]
        orderList = []

        for item in order:
            for card in actionCardsOnHand:
                if card.type == item:
                    orderList.append(card)

        discardSingleCard(orderList[0], game)


    else:
        discardSingleCard(actionCardsOnHand[0], game)


def specifyActionType(actiontype):
    takeAction = Action(type=actiontype,
                        explanation="no cards to discard")
    Connection.playAction(takeAction)


def discardSingleCard(card: Card, game: Game) -> Action:
    parsedCard = [vars(card)]

    if card.type == "nominate":
        nominatedPlayer = choosePlayerToNominate(game)

        # calculate nominated amount. If player has more cards a higher value gets nominated
        amount = nominatedPlayer.cardAmount // 3
        if amount < 1:
            amount = 1
        if amount > 3:
            amount = 3

        parsedPlayer = vars(nominatedPlayer)
        discardAction = Action(type="nominate",
                               explanation="random pick",
                               cards=parsedCard,
                               nominatedPlayer=parsedPlayer,
                               nominatedAmount=amount)

    else:
        discardAction = Action(type="discard",
                               explanation="random pick",
                               cards=parsedCard)

    return discardAction


def choosePlayerToNominate(game: Game) -> Player:
    playerlist = game.getPlayerList()
    cardAmountList = []

    for player in playerlist:
        cardAmountList.append(int(player.cardAmount))

    maxCards = max(cardAmountList)

    for player in playerlist:
        if maxCards == player.cardAmount:
            return player


def discardCardSet(topCard, matchedColors) -> Action:
    key = min(matchedColors)
    discardCardsList = []
    for i in range(topCard.value):
        discardCardsList.append(matchedColors[key][i])

    jsonCards = []
    for card in discardCardsList:
        parsedCard = vars(card)
        jsonCards.append(parsedCard)

    discardAction = Action(type="discard",
                           explanation="random pick",
                           cards=jsonCards)
    return discardAction


def matchCardsByColor(topCard: Card, playerCards: list) -> dict:
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


def checkForActionCards(matchedCards: dict) -> list:
    """ Check if current player has any action cards that are valid to discard

    :param matchedCards: List of current players cards completing a set
    :return: list of valid action cards
    """

    actionCardsList = []
    uniqueActionCards = []

    for color in matchedCards:
        for card in matchedCards[color]:
            if not card.type == "number":
                actionCardsList.append(card)
    print(actionCardsList)

    for card in actionCardsList:
        if card in uniqueActionCards:
            pass
        else:
            uniqueActionCards.append(card)

    return uniqueActionCards
