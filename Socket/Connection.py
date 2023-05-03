import socketio
import requests

# Repeatedly used URLS declared in shorter variables
baseURL = "http://nope.ddns.net/api/"
signinURL = baseURL + "signin"
signupURL = baseURL + "signup"

# Sent data declared as variables and saved as dictionary
# TODO: Refactor to have a user input
nameValue = "deedz"
pwValue = "deedz"
data = {'username': nameValue, 'password': pwValue}

# Socket IO Client
sio = socketio.Client()

def postRequest(url: str, data: dict) -> dict:
    """ Sends a POST request to a given URL with given data. Checks if response is successful.

     :param url: The URL to send the POST request to
     :type url: str
     :param data: The data to send in the body of the request. Contains specific keys and values
     :type data: dict

     :returns: the response body data in JSON format
     :rtype: dict

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
     :type responseBody: dict

     :returns: JSON Web Token as string
     :rtype: str

     """

    jwt = responseBody.get("jsonwebtoken")
    print("JWT Token extracted successfully:\n" + jwt)

    return jwt

@sio.event
def connect():
    """ Basic SocketIO event raised on connection """
    print("Client connected")

@sio.event
def connect_error():
    """ Basic SocketIO event raised on connection error """
    print("Connection failed")

@sio.event
def disconnect():
    """ Basic SocketIO event raised on disconnect """
    print("Client disconnected")


def connectToSocketIOServer(jwt: str):
    """ Tries to connect the client to the Socket IO Server

     :param jwt: The received access token
     :type jwt: str
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

class BearerAuth(requests.auth.AuthBase):
    """ Class to make authentication easier. Sends the JWT as a Bearer Token in the Header.

    Taken from https://requests.readthedocs.io/en/latest/user/authentication/#new-forms-of-authentication

    :returns: A formatted Bearer Token
    """

    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

def showUserConnections(jwt: str):
    """ Shows all currently connected users

    :param jwt: the JWT needed to authenticate the request
    :type jwt: str
    """

    users = requests.get("http://nope.ddns.net/api/userConnections", auth=BearerAuth(jwt))
    usersJSON = users.json()

    print("\nCurrently connected users:")
    for user in usersJSON:
        print(user.get("username"))


jwt = getJWTToken(postRequest(signinURL, data))
connectToSocketIOServer(jwt)
print("-----------------------")
showUserConnections(jwt)