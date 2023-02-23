import re
import setup_inf as si

class Neo84_app():

    def __init__(self):
        self.__version = '2023.2.1'
        self.app_name = '      > Tainted Wrench <'
        self.compat_version = '20.0.0'
        self.logo = [
            '                  _____   ___ ',
            '                 |  _  | /   |',
            ' _ __   ___  ___  \ V / / /| |',
            "| '_ \ / _ \/ _ \ / _ \/ /_| |",
            '| | | |  __/ (_) | |_| \___  |',
            '|_| |_|\___|\___/\_____/   |_/'
        ]

        self.__setup_inf = si.Setup_inf()

    def print_version(self):
        for line in self.logo:
            print(line)
        
        print(self.app_name)
        print('Package builder for Matrix42')
        print('Version:', self.version, 'for', self.compat_version)
        print('----------------------------')

    @property
    def version(self):
        return self.__version

    @property
    def setup_inf(self):
        return self.__setup_inf

    @setup_inf.setter
    def setup_inf(self, value):
        self.__setup_inf = value

    # inf line builder
    def __build_inf_line(self, key, value):
        # first line is an ini section without '='
        # just print the key name
        match = re.search('^\[.*', key)
        
        if (match != None):
            return key

                
        return str(key + ' = ' + value)

    def print_inf(self):
        meta_data = self.__setup_inf.inf[si.Package.meta_data]
        for key,value in meta_data.items():
            print(self.__build_inf_line(key, value))
            
        variables = self.__setup_inf.inf[si.Package.variables]
        print('')
        for key,value in variables.items():
            print(self.__build_inf_line(key, value))

        setup = self.__setup_inf.inf[si.Package.setup]
        print('')
        for key,value in setup.items():
            print(self.__build_inf_line(key, value))