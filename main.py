from Misc.User import User
from Socket import Connection
import sys
import Misc.Globals as glo


# baseURL = "http://nope.ddns.net/api/"


def main():
    """ Main function, handles basic user creation and connection to SocketIO
    """

    while True:
        print("Welcome to NOPE! Please choose if you want to SIGN IN or REGISTER")
        menuInput = input("[1] - SIGN IN\n[2] - REGISTER\n[3] - END\n")
        match menuInput:
            case "1":
                urlEndpoint = "signin"
                glo.user = Connection.setupUserAndConnection(urlEndpoint)
                if glo.user:
                    game(glo.user)
                break

            case "2":
                urlEndpoint = "signup"
                glo.user = Connection.setupUserAndConnection(urlEndpoint)
                if glo.user:
                    game(glo.user)
                break

            case "3":
                print("Goodbye!")
                exit()

            case _:
                print("Invalid input")


def game(user: User):
    """ Handles basic user menu to show players, start a game and disconnect from Server

    :param user: Current user object
    """
    print("\nWelcome to Nope!")

    while True:
        currentUsers = Connection.showUserConnections(user)
        print("Currently {number} players are connected.".format(number=len(currentUsers)))
        gameInput = input("\nWhat do you want to do?\n"
                          "[1] - Show current players\n"
                          "[2] - Create a game\n"
                          "[3] - Wait for invite\n"
                          "[4] - Create Tournament\n"
                          "[5] - Show game informations\n"
                          "[6] - Show tournament informations\n"
                          "[9] - End Game\n")

        match gameInput:
            case "1":
                print("\nCurrently connected users:")
                i = 0
                for users in currentUsers:
                    print("[{index}] ".format(index=i) + users.get("username"))
                    i += 1

            case "2":
                if len(currentUsers) >= 2:
                    startGame(user)
                    break
                else:
                    print("Not enough users to start a game!")

            case "3":
                Connection.sio.on("gameInvite", Connection.gameInvite)
                Connection.sio.wait()
                escape = input("Press key to exit")
                if escape:
                    break

            case "4":
                if len(currentUsers) >= 2:
                    startTournament(user)
                    break
                else:
                    print("Not enough users to start a game!")

            case "5":
                gameInfoMenu(user)

            case "9":
                Connection.sio.disconnect()
                break

            case _:
                print("Invalid input")


def gameInfoMenu(user: User):
    """ Handles the menuing to receive information of played games

    :param user: the current user
    """
    gameInfoInput = input("Do you want information of all games or a specific one?\n"
                          "[1] - All\n"
                          "[2] - Specific\n")
    match gameInfoInput:
        case "1":
            Connection.getRecentGames(user)

        case "2":
            gameIDInput = input("Input game ID:\n")
            Connection.getSpecificGameInfo(user, gameIDInput)


def startGame(user: User):
    """ Handles the basic menu for creating a game and specifying opponents and modifiers

    :param user: Current user object
    """
    noActionCards = False
    noWildcards = False
    oneMoreStartCard = False
    opponents = chooseOpponents(user)

    # TODO Add possible modifiers
    # modifiers = input("Do you want to modify your game?\n[1] - Yes\n[2] - No")
    # if modifiers == "1":
    #     while True:
    #         print("Current modifiers:")

    Connection.createGame(user, opponents)

def startTournament(user: User):

    opponents = chooseOpponents(user)

    mode = {"name": "round-robin", "numberOfRounds": 9}

    Connection.startTournament(user, mode, opponents)


def chooseOpponents(user):

    opponents = []
    challenge = input("Who would you like to challenge?\n"
                      "[1] - EVERYONE\n"
                      "[2] - SPECIFIC\n")
    currentUsers = Connection.showUserConnections(user)
    if challenge == "1":
        for opponent in currentUsers:
            opponents.append(opponent)
    if challenge == "2":
        print("Choose your opponents!")
        i = 0
        for users in currentUsers:
            print("[{index}] ".format(index=i) + users.get("username"))
            i += 1
        specificOpponents = []

        # Choose Opponents by number
        while True:
            try:
                index = int(input("Number of Opponent: "))
                if index < len(currentUsers):
                    specificOpponents.append(index)
                else:
                    print("Invalid input")

            except ValueError:
                break

        for opponent in specificOpponents:
            opponents.append(currentUsers[opponent])
    return opponents


if __name__ == '__main__':
    main()
