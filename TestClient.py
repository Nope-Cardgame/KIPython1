from Misc.User import User
from Socket import Connection
import sys
import Misc.Globals as glo

baseURL = "http://nope.ddns.net/api/"

def main():
    urlEndpoint = "signin"
    glo.user = connectTestUser(urlEndpoint)
    if glo.user:
        print("connected")
        Connection.sio.on("gameInvite", Connection.gameInvite)
        Connection.sio.wait()


def connectTestUser(urlEndpoint):
    username = "Dennis2"
    password = "dennis"
    user = User(username, password)

    response = Connection.postRequest(baseURL + urlEndpoint, user.loginData)
    jwt = Connection.getJWTToken(response)
    user.jwt = jwt
    Connection.connectToSocketIOServer(user, user.jwt)
    return user

main()
