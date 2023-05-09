import socketio
import requests
import Events
from Misc.User import User
from Misc.BearerAuth import BearerAuth

# Repeatedly used URLS declared in shorter variables
baseURL = "http://nope.ddns.net/api/"

# Sent data declared as variables and saved as dictionary
# TODO: Refactor to have a user input
nameValue = "deedz"
pwValue = "deedz"
data = {'username': nameValue, 'password': pwValue}

# Socket IO Client
sio = socketio.Client()


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
    print("JWT Token extracted successfully:\n" + jwt)

    return jwt


def connectToSocketIOServer(jwt: str):
    """ Tries to connect the client to the Socket IO Server

     :param jwt: The received access token
     """

    try:
        sio.connect(baseURL, auth={'token': jwt})
        print("My sid is: " + sio.sid)

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

    users = requests.get(baseURL + "userConnections", auth=BearerAuth(user.jwt))
    usersJSON = users.json()

    print("\nCurrently connected users:")
    for user in usersJSON:
        print(user.get("username"))

    return usersJSON


def createGame(user: User, players: dict, noActionCardsBool: bool = True, noWildcardsBool: bool = False,
               oneMoreStartCardsBool: bool = False):
    """ Create a game between defined Users. Optional game modifiers can be set.

        :param user: current user Object containing all data needed
        :param noActionCardsBool: Decide if game mode contains Action Cards
        :param noWildcardsBool: Decide if game mode contains Wildcards
        :param oneMoreStartCardsBool: Decide if game mode contains an additional starting card
        :param players: Dictionary of players competing in the game
        """

    # Parse arguments into body
    body = {"noActionCards": noActionCardsBool,
            "noWildcards": noWildcardsBool,
            "oneMoreStartCards": oneMoreStartCardsBool,
            "players": players
            }

    requests.post(baseURL + "game",
                  auth=BearerAuth(user.jwt),
                  json=body)

    # TODO: HANDLE GAMESTATE EVENT


def startTournament(user: User, mode: dict, players: dict):
    """ Starts a tournament in a specific mode

        :param user: Current user Object containing all data needed
        :param mode: Defines the tournament mode
        :param players: Dictionary of players competing in the game
        """

    body = {"modus": mode,
            "players": players
            }

    requests.post(baseURL + "tournament",
                  auth=BearerAuth(user.jwt),
                  json=body)

    # TODO: HANDLE TOURNAMENT EVENT

#
def getSpecificGameInfo(user: User, gameID: str) -> dict:
    """ Get information of a specific Game

        :param user: Current user Object containing all data needed
        :param gameID: The ID of the specific game
        """

    response = requests.get(baseURL + "game/" + gameID,
                        auth=BearerAuth(user.jwt))
    game =  response.json()
    print(game)
    # TODO: Write to .txt file


def getRecentGames(user: User):
    """ Get a List of all recently played games

        :param user: current user Object containing all data needed
        """

    response = requests.get(baseURL + "game",
                            auth=BearerAuth(user.jwt))
    recentGames = response.json()
    print(recentGames)
    # TODO: Write to .txt file



def tournamentList(user: User):
    """ Get a list of all recently played tournaments

        :param user: current user Object containing all data needed
        """
    response = requests.get(baseURL + "tournament",
                            auth=BearerAuth(user.jwt))
    game = response.json()
    print(game)
    # TODO: Write to .txt file


def getSpecificTournamentInfo(user: User, tournamentID: str):
    """ Get information of a specific tournament

        :param user: current user Object containing all data needed
        :param tournamentID:
        """
    response = requests.get(baseURL + "tournament/" + tournamentID,
                            auth=BearerAuth(user.jwt))
    game = response.json()
    print(game)
    # TODO: Write to .txt file
