from Misc.User import User

# def signin(user: User):
#     pass
#
# def signup(user: User):
#     pass

def main():
    print("Welcome to NOPE! Please choose if you want to SIGN IN or REGISTER")
    menuInput = input("[1] - SIGN IN\n[2] - REGISTER\n")
    match menuInput:
        case "1":
            username = input("Enter username: ")
            password = input("enter password: ")
            user = User(username, password)


        case "2":
            pass
        case _:
            print("Invalid input")
            main()


if __name__ == '__main__':
    main()
