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
    print("Client connected")

@sio.event
def connect_error():
    print("Connection failed")

@sio.event
def disconnect():
    print("Client disconnected")


def connectToSocketIOServer(jwt: str):
    """ Tries to connect the client to the Socket IO Server

     :param jwt: The received access token
     :type str:
     """

    try:
        sio.connect(baseURL, auth={'token': jwt})

    except requests.exceptions.RequestException as e:
        print(f'Failed to connect to SocketIO server: {e}')
    except socketio.exceptions.ConnectionError as e:
        print(f'Failed to connect to SocketIO server: {e}')
    except socketio.exceptions.BadNamespaceError as e:
        print(f'Failed to connect to SocketIO server: {e}')


jwt = getJWTToken(postRequest(signinURL, data))
connectToSocketIOServer(jwt)