from Misc.User import User
from Socket import Connection


# baseURL = "http://nope.ddns.net/api/"

def main():
    while True:
        print("Welcome to NOPE! Please choose if you want to SIGN IN or REGISTER")
        menuInput = input("[1] - SIGN IN\n[2] - REGISTER\n[3] - END\n")
        match menuInput:
            case "1":
                url = Connection.baseURL + "signin"
                username = input("Enter username: ")
                password = input("Enter password: ")
                user = User(username, password)
                connected = Connection.setupUserAndConnection(user, url, user.loginData)
                if connected:
                    game(user)

            case "2":
                url = Connection.baseURL + "signup"
                username = input("Enter username: ")
                password = input("enter password: ")
                newUser = User(username, password)
                connected = Connection.setupUserAndConnection(newUser, url, newUser.loginData)
                if connected:
                    game(newUser)

            case "3":
                print("Goodbye!")
                break

            case _:
                print("Invalid input")


def game(user: User):
    print("\nWelcome to Nope!")

    while True:
        # print("Currently {number} players are connected.\nWhat do you want to do?".format(number=len(Connection.showUserConnections(user))))
        gameInput = input("\nWhat do you want to do?\n[1] - Show current players\n[2] - Start a game\n")

        match gameInput:
            case "1":
                currentUsers = Connection.showUserConnections(user)

                print("\nCurrently " + str(len(currentUsers)) + " connected users:")
                i = 1
                for users in currentUsers:
                    print("[{index}] ".format(index=i) + users.get("username"))
                    i += 1

            case "2":
                print("Currently not available")

            case _:
                print("Invalid input")



def chooseGameMode():
    pass

if __name__ == '__main__':
    main()