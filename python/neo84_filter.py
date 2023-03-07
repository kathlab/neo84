from enum import IntEnum

# predefined filter lists
WIN_SYSENV_FILTER = [
    '%SystemRoot%',
    '%SYSTEMROOT%',
    '[sS]{1,1}ystem32',
]

# Generic filter for files, reg, etc.
class Filter_list():   
    def __init__(self, filter):
        self.__filter = filter

    @property
    def filter(self):
        return self.__filter

    @filter.setter
    def filter(self, value):
        self.__filter = value