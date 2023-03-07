# store system environment variables
class Sysenv_var():

    def __init__(self):
        self.__name = ''
        self.__values = []

    def __init__(self, name):
        self.__name = name
        self.__values = []

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def values(self):
        return self.__values

    @values.setter
    def values(self, values):
        self.__values = values