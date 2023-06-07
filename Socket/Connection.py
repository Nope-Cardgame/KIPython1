import socketio
import requests
from Misc.User import User
from Misc.BearerAuth import BearerAuth
from Misc.JSONObjects import *
from Logic import MainLogic
import Misc.Globals as glo

# Repeatedly used URL declared in shorter variables
baseURL = "http://nope.ddns.net/api/" #"https://deedz.flamtky.dev/api/"

# Socket IO Client
sio = socketio.Client()

# game = None


def setupUserAndConnection(urlEndpoint: str, ) -> User:
    """ Processes signin or signup of a user and connects him to the Server

    :param urlEndpoint: The url Endpoint to send the POST request to -> either signin or signup
    """

    username = input("Enter username: ")
    password = input("Enter password: ")
    user = User(username, password)

    response = postRequest(baseURL + urlEndpoint, user.loginData)
    jwt = getJWTToken(response)
    user.jwt = jwt
    connectToSocketIOServer(user, user.jwt)
    return user


def postRequest(url: str, data: dict) -> dict:
    """ Used for register and signup. Sends a POST request to a specific URL with given data. Checks if response is successful.

     :param url: The URL to send the POST request to
     :param data: The json data to send in the body of the request. Contains specific keys and values

     :returns: the response body data in JSON format
     """

    response = requests.post(url, data)
    responseCode = response.status_code

    if responseCode == 200:
        responseJSON = response.json()
        return responseJSON

    if (400 <= responseCode < 500):
        print("Client Error!\nResponse Code: " + str(responseCode))
        exit()


def getJWTToken(responseBody: dict) -> str:
    """ Extracts the JWT Token from a response body

     :param responseBody: the data of a prior response

     :returns: JSON Web Token as string
     """

    jwt = responseBody.get("jsonwebtoken")
    # print("JWT Token extracted successfully:\n" + jwt)

    return jwt


def connectToSocketIOServer(user: User, jwt: str):
    """ Tries to connect the client to the Socket IO Server

     :param user: The current User
     :param jwt: The received access token
     """

    try:
        sio.connect(baseURL, auth={'token': jwt})
        # print("My sid is: " + sio.sid)
        user.sid = sio.sid

    except requests.exceptions.RequestException as e:
        print(f'Failed to connect to SocketIO server: {e}')
    except socketio.exceptions.ConnectionError as e:
        print(f'Failed to connect to SocketIO server: {e}')
    except socketio.exceptions.BadNamespaceError as e:
        print(f'Failed to connect to SocketIO server: {e}')


def showUserConnections(user: User) -> dict:
    """ Shows all currently connected users

    :param user: current user Object containing all data needed
    """

    users = requests.get(baseURL + "userConnections",
                         auth=BearerAuth(user.jwt))
    usersJSON = users.json()

    return usersJSON


def createGame(user: User, players: list, noActionCardsBool: bool = False, noWildcardsBool: bool = False,
               oneMoreStartCardsBool: bool = False):
    """ Create a game between defined Users. Optional game modifiers can be set.

        :param user: current user Object containing all data needed
        :param noActionCardsBool: Decide if game mode contains Action Cards
        :param noWildcardsBool: Decide if game mode contains Wildcards
        :param oneMoreStartCardsBool: Decide if game mode contains an additional starting card
        :param players: List of players competing in the game
        """

    # Parse arguments into body
    body = {"noActionCards": noActionCardsBool,
            "noWildCards": noWildcardsBool,
            "oneMoreStartCards": oneMoreStartCardsBool,
            "players": players
            }

    response = requests.post(baseURL + "game",
                             auth=BearerAuth(user.jwt),
                             json=body)
    responseJSON = response.json()
    currentGame = Game(**responseJSON)

    # for player in currentGame.players:
    #     if player["username"] == user.name:
    #         user.sid = player["socketId"]

    sio.on("gameInvite", gameInvite)
    sio.wait()

    while True:
        sio.on("gameState", gameState)
        sio.wait()


def startTournament(user: User, mode: dict, players: list):
    """ Starts a tournament in a specific mode

        :param user: Current user Object containing all data needed
        :param mode: Defines the tournament mode
        :param players: Dictionary of players competing in the game
        """

    body = {"mode": mode,
            "participants": players
            }

    response = requests.post(baseURL + "tournament",
                             auth=BearerAuth(user.jwt),
                             json=body)

    sio.on("tournamentInvite", tournamentInvite)
    sio.wait()

    while True:
        sio.on("gameState", gameState)
        sio.wait()


def getSpecificGameInfo(user: User, gameID: str) -> dict:
    """ Get information of a specific Game

        :param user: Current user Object containing all data needed
        :param gameID: The ID of the specific game
        """

    response = requests.get(baseURL + "game/" + gameID,
                            auth=BearerAuth(user.jwt))
    game = response.json()
    print(game)
    # TODO: Write to .txt file or output


def getRecentGames(user: User):
    """ Get a List of all recently played games

        :param user: current user Object containing all data needed
        """

    response = requests.get(baseURL + "game",
                            auth=BearerAuth(user.jwt))
    recentGames = response.json()
    print(recentGames)
    # TODO: Output as List of GameIDs - maybe Write to .txt file


def tournamentList(user: User):
    """ Get a list of all recently played tournaments

        :param user: current user Object containing all data needed
        """
    response = requests.get(baseURL + "tournament",
                            auth=BearerAuth(user.jwt))
    game = response.json()
    print(game)
    # TODO: Output as List of GameIDs - maybe Write to .txt file


def getSpecificTournamentInfo(user: User, tournamentID: str):
    """ Get information of a specific tournament

        :param user: current user Object containing all data needed
        :param tournamentID:
        """
    response = requests.get(baseURL + "tournament/" + tournamentID,
                            auth=BearerAuth(user.jwt))
    game = response.json()
    print(game)
    # TODO: Write to .txt file or output


# Emitted Events:
def playAction(action):
    actionJSON = action.actionToDict()
    print(action.type + ": " + str(actionJSON))
    sio.emit("playAction", actionJSON)


def ready(accept: bool, gametype: str, invID: str):
    body = {"accept": accept,
            "type": gametype,
            "inviteId": invID}

    print("#### READY ####\n")
    sio.emit("ready", body)


# Received Events:
@sio.event
def connect():
    """ Basic SocketIO event raised on connection """
    print("Client connected")


@sio.event
def connect_error(data):
    """ Basic SocketIO event raised on connection error """
    print("Connection failed")


@sio.event
def disconnect():
    """ Basic SocketIO event raised on disconnect """
    print("Client disconnected")


@sio.on("gameState")
def gameState(data):
    game = Game(**data)

    if game.state == "game_start":
        print("Game starting")
    if gameState == "game_end":
        print("Game Over")
    if gameState == "cancelled":
        print("Game Cancelled")
    else:
        if glo.user.name == game.currentPlayer["username"]:
            print("\nYour turn:")
            MainLogic.main(game)


@sio.on("error")
def error(data):
    print("An error occured")
    print(data)


@sio.on("banned")
def banned(data):
    print("You have been banned")


@sio.on("gameEnd")
def gameEnd(data):
    print('\x1b[6;30;42m' + "Game ended" + '\x1b[0m')

    game = Game(**data)
    player = game.getPlayerByName(glo.user.name)
    print('\x1b[6;30;42m' + "Rank: " + str(player.ranking) + "/" + str(len(game.players)) + '\x1b[0m')


@sio.on("tournamentInvite")
def tournamentInvite(data):
    print("Tournament Invite received\n")
    # tournament = Tournament(**data)
    tournID = data["id"]

    while True:
        acceptInvite = input("Accept Invite? y/n\n")

        match acceptInvite:
            case "y":
                ready(True, "tournament", tournID)
                break

            case "n":
                ready(False, "tournament", tournID)
                break

            case _:
                print("Invalid Input")


@sio.on("eliminated")
def eliminated(data):
    print('\x1b[6;30;41m' + "You have been eliminated" + '\x1b[0m')
    print(data)


@sio.on("gameInvite")
def gameInvite(data):
    print("Game invite received\n")
    game = Game(**data)
    invID = game.id

    while True:
        acceptInvite = input("Accept Invite? y/n\n")

        match acceptInvite:
            case "y":
                ready(True, "game", invID)
                break

            case "n":
                ready(False, "game", invID)
                break

            case _:
                print("Invalid Input")
