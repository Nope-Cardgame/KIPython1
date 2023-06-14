class User:
    """ Class that represents the current user of the Client """

    def __init__(self,
                 name: str,
                 password: str):
        """ Construct the User Object by setting a name and password. Parses these into a dict to store information

        :param name: Input of the users name
        :param password: Input of the users password
        """

        loginDataJSON = {"username": name, "password": password}
        self.name = name
        self.password = password
        self.loginData = loginDataJSON
        self.jwt = None
        self.sid = None

    def __getattr__(self, item):
        return self.__dict__[f"_{item}"]

    def __setattr__(self, key, value):
        self.__dict__[f"_{key}"] = value

