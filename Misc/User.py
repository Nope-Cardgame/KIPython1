class User:

    def __init__(self, name: str, password: str):
        loginDataJSON = {"username": name, "password": password}
        self.name = name
        self.password = password
        self.loginData = loginDataJSON
        self.jwt = None

    def __getattr__(self, item):
        return self.__dict__[f"_{item}"]

    def __setattr__(self, key, value):
        self.__dict__[f"_{key}"] = value

