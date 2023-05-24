import requests

class BearerAuth(requests.auth.AuthBase):
    """ Class to make authentication easier. Transforms the JWT to a Header containing a Bearer Token.

    Taken from https://requests.readthedocs.io/en/latest/user/authentication/#new-forms-of-authentication

    :returns: A Bearer Token formatted as Authorization Header
    """

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r
