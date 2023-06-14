class Card:
    """ Class to represent a single card object """

    def __init__(self,
                 type: str,
                 colors: list,
                 name: str,
                 value: int = None):
        """ Constructs the Card object. Set a cards type, colors, name and value

        :param type: Type of Card - e.g. Number or Nominate
        :param colors: List of the cards colors. Can be up to 4 different ones
        :param name: Name of the specific card
        :param value: Value of specific card
        """
        self.type = type
        self.colors = colors
        self.name = name
        self.value = value

    def cardToDict(self):
        """ Parse the Card object to a Dictionary. Attributes with None are not used

        :return: The Card as a dict/JSON
        """

        actionDict = vars(self)
        res = {k: v for k, v in actionDict.items() if v is not None}
        return res


class Player:
    """ Class that represents a player object """

    def __init__(self,
                 username: str,
                 socketId: str,
                 cardAmount: int,
                 cards: list[dict] = None,
                 disqualified: bool = None,
                 accepted: bool = None,
                 ranking: int = None):
        """ Constructs the Player object. Sets needed parameters

        :param username: The players username
        :param socketId: The players sid
        :param cardAmount: Amount of cards the player holds in his hand
        :param cards: List of cards the player holds in his hand
        :param ranking: Current ranking of player
        :param disqualified: Bool if player is disqualified
        :param accepted: Bool if current player accepted the invite
        """

        self.username = username
        self.socketId = socketId
        self.cardAmount = cardAmount
        self.cards = cards
        self.ranking = ranking
        self.disqualified = disqualified
        self.accepted = accepted

    def getCards(self):
        """ Gets the players current cards and parses them to Card objects

        :return: list of Card objects
        """

        cardsList = []
        for cardData in self.cards:
            card = Card(**cardData)
            cardsList.append(card)

        return cardsList

    def toDict(self):
        """ Parse the Player object to a Dictionary. Attributes with None are not used

        :return: The Player as a dict/JSON
        """

        playerDict = vars(self)
        res = {k: v for k, v in playerDict.items() if v is not None}
        return res


class TournamentParticipant:
    """ Class that represents a participant in a tournament"""

    def __init__(self,
                 username: str,
                 socketId: str,
                 ranking: int,
                 disqualified: bool,
                 score: int,
                 accepted: bool = None):
        """ Construct the participants in a tournament

        :param username: Participants name
        :param socketId: Participants socket ID
        :param ranking: Participants current rank
        :param disqualified: Bool if participant is disqualified
        :param score: Current score of participant
        :param accepted: bool if participant accepted the invite
        """

        self.username = username
        self.socketId = socketId
        self.ranking = ranking
        self.disqualified = disqualified
        self.score = score
        self.accepted = accepted


class Tournament:
    """ Class that represents a Tournament """

    def __init__(self,
                 id: str,
                 mode: dict,
                 state: str,
                 participants: list[dict],
                 games: list[dict],
                 startTime: str = None,
                 endTime: str = None,
                 noActionCards: bool = None,
                 noWildCards: bool = None,
                 oneMoreStartCard: bool = None,
                 actionTimeout: str = None,
                 invitationTimeout: str = None,
                 startWithRejection: bool = None,
                 sendGameInvite: bool = None,
                 participantAmount: str = None,
                 gameAmount: str = None):
        """ Construct a tournament object with given details

        :param id: The tournaments ID
        :param mode: Current game mode
        :param state: The current tournament state
        :param participants: List of all Participants
        :param games: List of all games from current tournament
        :param startTime: Starting time of Tournament
        :param endTime: End of tournament
        :param noActionCards: Bool if ActionCards are part of the game
        :param noWildCards: Bool if WildCards are part of the game
        :param oneMoreStartCard: Bool if players begin with a additional Card
        :param actionTimeout: Server stats - only before and in game
        :param invitationTimeout: Server stats - only before and in game
        :param startWithRejection: Server stats - only before and in game
        :param sendGameInvite: bool if invite is sent - only in prep and ongoing state
        :param participantAmount: Number of participating players
        :param gameAmount: the number of games played
        """

        self.id = id
        self.mode = mode
        self.participants = participants
        self.state = state
        self.games = games
        self.startTime = startTime
        self.endTime = endTime
        self.actionTimeout = actionTimeout
        self.invitationTimeout = invitationTimeout
        self.startWithRejection = startWithRejection
        self.playerAmount = participantAmount
        self.noActionCards = noActionCards
        self.noWildCards = noWildCards
        self.sendGameInvite = sendGameInvite
        self.gameAmount = gameAmount
        self.oneMoreStartCard = oneMoreStartCard

    def getParticipantByName(self, name) -> TournamentParticipant:
        """ Get a participant of the tournament by name. Parses the particitpant to a TournamentParticipant object

        :param name: the name of the wanted participant
        :return: Participant as TournamentParticipant object
        """

        for playerData in self.participants:
            if playerData["username"] == name:
                player = TournamentParticipant(**playerData)
                return player


class Action:
    """ Class that represents the Action a player can send """

    def __init__(self,
                 type: str,
                 explanation: str,
                 player: dict = None,
                 nominatedAmount: int = None,
                 cards: list[dict] = None,
                 nominatedPlayer: dict = None,
                 nominatedColor: str = None):
        """ Construct the Action object for the player to send

        :param type: The type of action the player wants to perform
        :param explanation: Explanation of the chosen action
        :param player: The current player
        :param nominatedAmount: The amount of cards taken/discarded
        :param cards: List of cards taken/discarded
        :param nominatedPlayer: The chosen player that is nominated if Nominate Card is played
        :param nominatedColor: The card that is nominated if Nominate Card is played
        """

        if type not in ["take", "discard", "nope", "nominate"]:
            raise ValueError("Invalid Action Type!")

        self.type = type
        self.explanation = explanation
        self.player = player
        self.nominatedAmount = nominatedAmount
        self.cards = cards
        self.nominatedPlayer = nominatedPlayer
        self.nominatedColor = nominatedColor

    def actionToDict(self) -> dict:
        """ Parses a Action object to a Dictionary/JSON. Attributes that are None are not parsed

        :return: Dictionary of the action
        """

        actionDict = vars(self)
        res = {k: v for k, v in actionDict.items() if v is not None}
        return res


class Game:
    """ Class that represents a Game """

    def __init__(self,
                 id: str,
                 state: str,
                 noActionCards: bool,
                 noWildCards: bool,
                 oneMoreStartCard: bool,
                 players: list[dict],
                 actionTimeout: str = None,
                 invitationTimeout: str = None,
                 startWithRejection: bool = None,
                 startTime: str = None,
                 tournament: dict = None,
                 gameRole: str = None,
                 encounterRound: str = None,
                 playerAmount: str = None,
                 discardPile: list[dict] = None,
                 lastAction: dict = None,
                 lastNominateAmount: int = None,
                 lastNominateColor: str = None,
                 currentPlayer: dict = None,
                 initialTopCard: dict = None,
                 actions: list[dict] = None,
                 endTime: str = None):
        """ Constructor for a Game object

        :param id: ID of current game
        :param state: Current state of game
        :param noActionCards: Bool if ActionCards are part of the game
        :param noWildCards: Bool if WildCards are part of the game
        :param oneMoreStartCard: Bool if players begin with a additional Card
        :param players: List of Players participating in a game
        :param actionTimeout: Server stats - only before and in game
        :param invitationTimeout: Server stats - only before and in game
        :param startWithRejection: Server stats - only before and in game
        :param startTime: Starting time of game
        :param tournament: (Optional) Tournament object if game is in tournament mode
        :param gameRole: (Optional) Game modifiers like sudden death in tournament mode
        :param encounterRound: (Optional) current round of tournament
        :param playerAmount: Number of players connected to the game - populated by server
        :param discardPile: List of discarded cards - only if game is running
        :param lastAction: The last played Action - only if game is running
        :param lastNominateAmount: The last nominated amount - only if game is running
        :param lastNominateColor: The last nominated color - only if game is running
        :param currentPlayer: The current player - only if game is running
        :param initialTopCard: The top card at the end of a game - only if game is finished
        :param actions: List of all Actions performed - only if game is finished
        :param endTime: End time of the game - only if game is finished
        """

        # Check for invalid game states
        if state not in ["game_start",
                         "nominate_flipped",
                         "turn_start",
                         "card_drawn",
                         "game_end",
                         "cancelled",
                         "preparation"]:
            raise ValueError("Invalid Gamestate!")

        self.id = id
        self.state = state
        self.noActionCards = noActionCards
        self.noWildCards = noWildCards
        self.oneMoreStartCard = oneMoreStartCard
        self.tournament = tournament
        self.gameRole = gameRole
        self.encounterRound = encounterRound
        self.players = players
        self.discardPile = discardPile
        self.lastAction = lastAction
        self.lastNominateAmount = lastNominateAmount
        self.lastNominateColor = lastNominateColor
        self.currentPlayer = currentPlayer
        self.startTime = startTime
        self.initialTopCard = initialTopCard
        self.actions = actions
        self.endTime = endTime
        self.actionTimeout = actionTimeout
        self.invitationTimeout = invitationTimeout
        self.startWithRejection = startWithRejection
        self.playerAmount = playerAmount

    def getPlayerList(self) -> list:
        """ Function to parse all participating players to Player objects and add them to a list

        :return: a list of Player objects containing all participating players
        """

        playerList = []

        for playerData in self.players:
            player = Player(**playerData)
            playerList.append(player)

        return playerList

    def getPlayer(self, sid) -> Player:
        """ Function to get a single player by his sid and parse them to a Player object

        :param sid: socketID of the wanted player
        :return: The wanted player as a Player object
        """

        for playerData in self.players:
            if playerData["socketId"] == sid:
                player = Player(**playerData)
                return player

    def getPlayerByName(self, name) -> Player:
        """ Function to get a single player by his name and parse them to a Player object

        :param name: name of the wanted player
        :return: The wanted player as a Player object
        """

        for playerData in self.players:
            if playerData["username"] == name:
                player = Player(**playerData)
                return player

    def getDiscardPile(self) -> list:
        """ Function to get the discard pile and parse all cards to Card objects

        :return: a list of Card objects, currently on the discard pile
        """

        discardPileList = []

        for cardData in self.discardPile:
            card = Card(**cardData)
            discardPileList.append(card)
        return discardPileList

    def getTopCard(self) -> Card:
        """ Function to get the top card of the discard pile and parse it to a Card object

        :return: The top card as Card object
        """

        topCard = Card(**self.discardPile[0])
        return topCard

    def getCurrentPlayer(self) -> Player:
        """ Function to get the current player and parse them to a Player object

        :return: Current player as Player object
        """

        player = Player(**self.currentPlayer)
        return player
