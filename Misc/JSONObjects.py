class Card:
    """ Class to represent a single card object """

    def __init__(self,
                 type: str,
                 color: list,
                 name: str,
                 value: int = None):
        """ Constructs the Card object. Set a cards type, colors, name and value

        :param type: Type of Card - e.g. Number or Nominate
        :param color: List of the cards colors. Can be up to 4 different ones
        :param name: Name of the specific card
        :param value: Value of specific card
        """
        self.type = type
        self.color = color
        self.name = name
        self.value = value

class Player:
    """ Class that represents a player object """

    def __init__(self,
                 username: str,
                 socketID: str,
                 cardAmount: int,
                 cards: list,
                 ranking: int,
                 disqualified: bool):
        """ Constructs the Player object. Sets needed parameters

        :param username: The players username
        :param socketID: The players sid
        :param cardAmount: Amount of cards the player holds in his hand
        :param cards: List of cards the player holds in his hand
        :param ranking: Current ranking of player
        :param disqualified: Bool if player is disqualified
        """

        self.username = username
        self.socketID = socketID
        self.cardAmount = cardAmount
        self.cards = cards
        self.ranking = ranking
        self.disqualified = disqualified


class TournamentParticipant:
    """ Class that represents a participant in a tournament"""

    def __init__(self,
                 username: str,
                 ranking: int,
                 disqualified: bool,
                 score: int):
        """ Construct the participants in a tournament

        :param username: Participants name
        :param ranking: Participants current rank
        :param disqualified: Bool if participant is disqualified
        :param score: Current score of participant
        """

        self.username = username
        self.ranking = ranking
        self.disqualified = disqualified
        self.score = score


class Tournament:
    """ Class that represents a Tournament """

    def __init__(self,
                 id: int,
                 mode: dict,
                 participants: list,
                 games: list,
                 startTime: str,
                 endTime: str):
        """ Construct a tournament object with given details

        :param id: The tournaments ID
        :param mode: Current game mode
        :param participants: List of all Participants
        :param games: List of all games from current tournament
        :param startTime: Starting time of Tournament
        :param endTime: End of tournament
        """

        self.id = id
        self.mode = mode
        self.participants = participants
        self.games = games
        self.startTime = startTime
        self.endTime = endTime


class Actions:
    """ Class that represents the Action a player can send """

    def __init__(self,
                 type: str,
                 explanation: str,
                 player: Player,
                 amount: int = None,
                 cards: list = None,
                 nominatedPlayer: Player = None,
                 nominatedCard: Card = None):
        """ Construct the Action object for the player to send

        :param type: The type of action the player wants to perform
        :param explanation: Explanation of the chosen action
        :param player: The current player
        :param amount: The amount of cards taken/discarded
        :param cards: List of cards taken/discarded
        :param nominatedPlayer: The chosen player that is nominated if Nominate Card is played
        :param nominatedCard: The card that is nominated if Nominate Card is played
        """

        if type not in ["take", "discard", "nope", "nominate"]:
            raise ValueError("Invalid Action Type!")

        self.type = type
        self.explanation = explanation
        self.player = player
        self.amount = amount
        self.cards = cards
        self.nominatedPlayer = nominatedPlayer
        self.nominatedCard = nominatedCard


class Game:
    """ Class that represents a Game """

    def __init__(self,
                 id: int,
                 state: str,
                 noActionCards: bool,
                 noWildCards: bool,
                 oneMoreStartCard: bool,
                 players: list,
                 startTime: str,
                 tournament: Tournament = None,
                 gameRole: str = None,
                 encounterRound: int = None,
                 discardPile: list = None,
                 lastAction: Actions = None,
                 currentPlayer: Player = None,
                 initialTopCard: Card = None,
                 actions: list = None,
                 endTime: str = None):
        """ Constructor for a Game object

        :param id: ID of current game
        :param state: Current state of game
        :param noActionCards: Bool if ActionCards are part of the game
        :param noWildCards: Bool if WildCards are part of the game
        :param oneMoreStartCard: Bool if players begin with a additional Card
        :param players: List of Players participating in a game
        :param startTime: Starting time of game
        :param tournament: (Optional) Tournament object if game is in tournament mode
        :param gameRole: (Optional) Game modifiers like sudden death in tournament mode
        :param encounterRound: (Optional) current round of tournament
        :param discardPile: List of discarded cards - only if game is running
        :param lastAction: The last played Action - only if game is running
        :param currentPlayer: The current player - only if game is running
        :param initialTopCard: The top card at the end of a game - only if game is finished
        :param actions: List of all Actions performed - only if game is finished
        :param endTime: End time of the game - only if game is finished
        """

        if state not in ["game_start",
                         "nominate_flipped",
                         "turn_start",
                         "card_drawn",
                         "game_end",
                         "cancelled"]:
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
        self.currentPlayer = currentPlayer
        self.startTime = startTime
        self.initialTopCard = initialTopCard
        self.actions = actions
        self.endTime = endTime
