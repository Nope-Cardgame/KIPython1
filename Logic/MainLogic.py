from Misc.JSONObjects import *
from Socket import Connection
import random


def main(game: Game):
    """ Start the Main AI Logic and make a move
    """

    player = game.getCurrentPlayer()

    # Check if user is disqualified
    if not player.disqualified:
        playerCards = player.getCards()

        topCard = checkTopCardForActionCards(game.getDiscardPile(), game, 0)
        print("current top card: " + topCard.name + " -- " + str(topCard.cardToDict()))

        cardMatches = matchCardsByColor(topCard, playerCards)
        actionCardsOnHand = checkForActionCards(cardMatches)

        # When turn starts check for matching pairs - discard matches or take a card
        makeMove(actionCardsOnHand, cardMatches, topCard, game)


def checkTopCardForActionCards(discardPile: list, game: Game, index: int) -> Card:
    """ Check if the current TopCard is a action card and return it. Includes logic to check if the TopCard is
    played a the initial card or if a Invisible card is played.

    :param discardPile: The games discard pile
    :param game: The current Game
    :param index: Index used to search discard Pile on recursion. Starts at 0 -> TopCard of the pile
    :return: The current TopCard as a Card object
    """

    topCard = discardPile[index]

    # check if the current top card of the pile is the initial card.
    if len(discardPile) - index <= 1:
        print("INITIAL TOP CARD")

        # Match case to set missing attributes (like value and colors) of the top card in case it is the initial one
        match topCard.type:
            case "invisible":
                topCard.value = 1

            case "reset":
                topCard.value = 1
                topCard.colors = ["red", "green", "blue", "yellow"]

            # Logic for a initial Nominate TopCard or in case it's revealed by a invisible
            case "nominate":

                # nominate_flipped state is only sent if nominate card is the initital card - Players can make a move as
                # if they played it themselves
                if game.state == "nominate_flipped":
                    action = nominatePlayer(topCard, game)
                    Connection.playAction(action)

                # If the nominate card is revealed by a invisible card the value is set to the last nominated value
                # if it's a multi nominate the color is also set to the last nominated color
                else:
                    topCard.value = game.lastNominateAmount
                    if topCard.name == "multi nominate":
                        topCard.colors = [game.lastNominateColor]

            case "number":
                pass

        return topCard

    else:
        match topCard.type:

            # in case of a Invisible card the index is incremented and the function is called recursively. That way it
            # can handle multiple invisible cards
            case "invisible":
                for card in range(index, len(discardPile)):
                    index += 1
                    topCard = checkTopCardForActionCards(discardPile, game, index)
                    return topCard

            case "reset":
                topCard.value = 1
                topCard.colors = ["red", "green", "blue", "yellow"]

            case "nominate":
                topCard.value = game.lastNominateAmount
                if topCard.name == "multi nominate":
                    topCard.colors = [game.lastNominateColor]

            case "number":
                pass

        return topCard


def makeMove(actionCardsOnHand: list, cardMatches: dict, topCard: Card, game: Game):
    """ Function to decide on a move. Checks if cards can be discarded - if not it either sends
    a take or nope event to the server

    :param actionCardsOnHand: List of the Action Cards currently on hand
    :param cardMatches: Dict of cards that match the TopCards requirements
    :param topCard: The top card of the discard pile
    :param game: Current Game object
    """

    # checks if there are any cards that match the TopCards requirements
    if cardMatches:
        # if there are action cards on the players hand, one of those will be played instead of a set
        if actionCardsOnHand:
            discardActionCard = playActionCard(actionCardsOnHand, game)
            Connection.playAction(discardActionCard)
        else:
            discardAction = discardCardSet(topCard, cardMatches)
            Connection.playAction(discardAction)

    else:
        match game.state:
            case "turn_start":
                specifyActionType("take")
            case "card_drawn":
                specifyActionType("nope")


def playActionCard(actionCardsOnHand: list, game: Game) -> Action:
    """ Decide on a Action if a action Card is on hand and shall be played.
    If multiple cards are available the Action cards have a order in which the will be played.

    :param actionCardsOnHand: List of the actionCards on players hand
    :param game: The current Game object
    """

    if len(actionCardsOnHand) > 1:

        order = ["nominate", "invisible", "reset"]
        orderList = []

        for item in order:
            for card in actionCardsOnHand:
                if card.type == item:
                    orderList.append(card)

        action = discardSingleCard(orderList[0], game)

    else:
        action = discardSingleCard(actionCardsOnHand[0], game)

    return action


def specifyActionType(actiontype: str):
    """ Sends a playAction Event with a given string.

    :param actiontype: Either "take" or "nope"
    """

    specificAction = Action(type=actiontype,
                            explanation="no cards to discard")
    Connection.playAction(specificAction)


def nominatePlayer(topCard: Card, game: Game) -> Action:
    """ Function that returns a nominate Action in case a nominate card is flipped as the initial card of the
    discard pile. in this case no cards from the hand will be played.

    :param topCard: The Card that will be played - a Card object of a Action Card
    :param game: The current Game object
    :return: A Action object containing all required attributes like nominatedPlayer, amount and nominatedColor
    """

    nominatedPlayer = choosePlayerToNominate(game)

    # calculate nominated amount. If player has more cards a higher value gets nominated
    amount = nominatedPlayer.cardAmount // 3
    if amount < 1:
        amount = 1
    if amount > 3:
        amount = 3

    # Check if the card is a multi nominate - if yes it also needs a nominated color
    if topCard.name == "multi nominate":

        nominatedColor = nominateColor()

        parsedPlayer = nominatedPlayer.toDict()
        discardAction = Action(type="nominate",
                               explanation="random pick",
                               cards=None,
                               nominatedPlayer=parsedPlayer,
                               nominatedAmount=amount,
                               nominatedColor=nominatedColor)
        print("nominated player: " + nominatedPlayer.username + " - nominated Amount: " + str(amount) + " - nominated color:")

    # if not only a player and amount will be added to Action
    else:
        parsedPlayer = nominatedPlayer.toDict()
        discardAction = Action(type="nominate",
                               explanation="random pick",
                               cards=None,
                               nominatedPlayer=parsedPlayer,
                               nominatedAmount=amount)
        print("nominated player: " + nominatedPlayer.username + " - nominated Amount: " + str(amount))

    return discardAction


def nominateColor() -> str:
    """ Function to choose a random string from the possible colors to nominate
    """

    possiblecolors = ["red", "green", "yellow", "blue"]
    randomColor = random.choice(possiblecolors)
    return randomColor


def discardSingleCard(card: Card, game: Game) -> Action:
    """ Function to create a Action to play a single card. Used to play Action Cards.

    :param card: The Card object that will be played
    :param game: The current Game object
    :return: Action object containing all the required attributes of the move
    """

    parsedCard = [card.cardToDict()]

    # check for nominate cards and choose a player and amount
    if card.type == "nominate":
        nominatedPlayer = choosePlayerToNominate(game)

        # calculate nominated amount. If player has more cards a higher value gets nominated
        amount = nominatedPlayer.cardAmount // 3
        if amount < 1:
            amount = 1
        if amount > 3:
            amount = 3

        # if card is a multi nominate also select a color to nominate
        if card.name == "multi nominate":

            nominatedColor = nominateColor()
            parsedPlayer = nominatedPlayer.toDict()
            discardAction = Action(type="nominate",
                                   explanation="play multi nomiante",
                                   cards=parsedCard,
                                   nominatedPlayer=parsedPlayer,
                                   nominatedAmount=amount,
                                   nominatedColor=nominatedColor)
            print("played ActionCard: " + card.type + " - nominated Amount: " + str(amount) + " - nominated color:")

        else:
            parsedPlayer = nominatedPlayer.toDict()
            discardAction = Action(type="nominate",
                                   explanation="play nominate",
                                   cards=parsedCard,
                                   nominatedPlayer=parsedPlayer,
                                   nominatedAmount=amount)
            print("played ActionCard: " + card.type + " - nominated Amount: " + str(amount))

    else:
        discardAction = Action(type="discard",
                               explanation="discard cards",
                               cards=parsedCard)
        print("played ActionCard: " + card.type)

    return discardAction


def choosePlayerToNominate(game: Game) -> Player:
    """ Function to determine which player will be nominated. Selects player with most cards and ignores
    the current player.

    :param game: The current Game object
    :return: A Player object of the player to nominate
    """

    playerlist = game.getPlayerList()
    currentPlayer = game.getCurrentPlayer()
    cardAmountList = []

    for player in playerlist:
        if player.username != currentPlayer.username:
            cardAmountList.append(int(player.cardAmount))

    maxCards = max(cardAmountList)

    for player in playerlist:
        if maxCards == player.cardAmount and player.username != currentPlayer.username:
            return player


def discardCardSet(topCard: Card, matchedColors: dict) -> Action:
    """ Function to determine which cards to discard. The set with less matching cards will be discarded, to minimize
    the chance of repetitive matches

    :param topCard: The current top Card of the discard pile
    :param matchedColors: Dict of all matching card sets ordered by color as key
    :return: Action object containing the attributes needed to make a move
    """

    key = min(matchedColors)
    discardCardsList = []
    for i in range(topCard.value):
        discardCardsList.append(matchedColors[key][i])

    jsonCards = []
    for card in discardCardsList:
        parsedCard = card.cardToDict()
        jsonCards.append(parsedCard)

    discardAction = Action(type="discard",
                           explanation="random pick",
                           cards=jsonCards)
    return discardAction


def matchCardsByColor(topCard: Card, playerCards: list) -> dict:
    """ Check the players cards for completed sets, depending on the top card

    :param topCard: The current top card
    :param playerCards: The current players cards
    :return: Dictionary of matching cards which complete a required set - with colors as keys and a list of Cards as value
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

    for card in actionCardsList:
        if card in uniqueActionCards:
            pass
        else:
            uniqueActionCards.append(card)

    return uniqueActionCards
