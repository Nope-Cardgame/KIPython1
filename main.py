from Misc.User import User
from Socket import Connection
import sys


# baseURL = "http://nope.ddns.net/api/"

def main():
    while True:
        print("Welcome to NOPE! Please choose if you want to SIGN IN or REGISTER")
        menuInput = input("[1] - SIGN IN\n[2] - REGISTER\n[3] - END\n")
        match menuInput:
            case "1":
                urlEndpoint = "signin"
                user = Connection.setupUserAndConnection(urlEndpoint)
                if user:
                    game(user)
                break

            case "2":
                urlEndpoint = "signup"
                user = Connection.setupUserAndConnection(urlEndpoint)
                if user:
                    game(user)
                break

            case "3":
                print("Goodbye!")
                exit()

            case _:
                print("Invalid input")


def game(user: User):
    print("\nWelcome to Nope!")

    while True:
        print("Currently {number} players are connected.".format(number=len(Connection.showUserConnections(user))))
        gameInput = input("\nWhat do you want to do?\n"
                          "[1] - Show current players\n"
                          "[2] - Start a game\n"
                          "[9] - End Game\n")

        match gameInput:
            case "1":
                currentUsers = Connection.showUserConnections(user)

                print("\nCurrently connected users:")
                i = 0
                for users in currentUsers:
                    print("[{index}] ".format(index=i) + users.get("username"))
                    i += 1

            case "2":
                startGame(user)

            case "9":
                Connection.sio.disconnect()
                break

            case _:
                print("Invalid input")


def startGame(user: User):

    opponents = []
    noActionCards = False
    noWildcards = False
    oneMoreStartCard = False

    challenge = input("Who would you like to challenge?\n"
          "[1] - EVERYONE\n"
          "[2] - SPECIFIC\n")

    currentUsers = Connection.showUserConnections(user)
    if challenge == "1":
        for opponent in currentUsers:
            opponents.append(currentUsers[opponent])

    if challenge == "2":
        print("Choose your opponents! Input 'q' to quit")
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

    # TODO Add possible modifiers
    # modifiers = input("Do you want to modify your game?\n[1] - Yes\n[2] - No")
    # if modifiers == "1":
    #     while True:
    #         print("Current modifiers:")

    Connection.createGame(user, opponents)



if __name__ == '__main__':
    main()
