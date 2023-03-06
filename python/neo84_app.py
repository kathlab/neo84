from neo84_print import sprint
from os.path import join, getsize
import neo84_task as task
import os
import re
import setup_inf as si
import shutil

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

        self.__setup_inf = si.Setup_inf() # setup.inf structure
        self.__task = task.Neo84_task()   # task for action

    # inf line builder. construct lines with and without values
    # first element is always an ini section that has no '='
    # also elements that are a list (filenames, reg entries) have no '='
    def __build_inf_line(self, key, value):
        
        # just print the key name
        # if line is...
        # ...[IniSection]
        # ...; Comment
        # ...HK?? registry entry
        # ...#???:???? matrix42 specific action to define a link to a [IniSection]
        # ...?: file entry

        match = re.search('^\[|^;|^HK[CRLM]{2}|^#|^[0-9]{1}:', key)
        if (match != None):
            return key

        # everything else has a value
        return str(key + ' = ' + value)

    def print_version(self):
        for line in self.logo:
            print(line)
        
        print(self.app_name)
        print('Package builder for Matrix42')
        print('Version:', self.version, 'for', self.compat_version)
        print('----------------------------')

    ###########################################################################

    @property
    def version(self):
        return self.__version

    @property
    def setup_inf(self):
        return self.__setup_inf

    @setup_inf.setter
    def setup_inf(self, value):
        self.__setup_inf = value

    @property
    def task(self):
        return self.__task

    @task.setter
    def task(self, value):
        self.__task = value

    ###########################################################################

    def generate_inf(self):
        inf = []

        # set meta_data from task
        self.__setup_inf.inf[si.Package.meta_data]['Author'] = self.__task.author
        self.__setup_inf.inf[si.Package.meta_data]['CreationDate'] = self.__task.date
        self.__setup_inf.inf[si.Package.meta_data]['Tested on'] = self.__task.os
        self.__setup_inf.inf[si.Package.meta_data]['Build'] = self.__task.build

        for package_section in range(0, 21):
            entries = self.__setup_inf.inf[package_section]
            inf.append('')
            for key,value in entries.items():
                inf.append(self.__build_inf_line(key, value))

        return inf
    
    # add all registry additions from Diff.inf
    def add_diff_reg(self, file_name):
        
        with open(file_name, 'r') as file:
            
            # registry additions are the most mandatory
            # everything else can be ignored
            # first, find this entry, then collect all reg adds
            line_found = False
            reference_pos = 0
            for line in file:
                sprint('.', new_line='')

                # find reg adds start line
                match = re.search('^\[AddReg\]', line)
                if (match != None):
                    line_found = True
                    #reference_pos = file.tell()
                    break

            # let's check if we got anything
            if (line_found == False):
                raise Exception('add_diff_reg() - file does not contain [AddReg]')

            # process reg ads
            for line in file:

                match = re.search('^HK[CRLM]{2},', line)
                if (match != None):
                    # add to list but remove line breaks
                    self.__setup_inf.inf[si.Package.reg_product][line.replace('\n', '')] = ''
                    sprint('#', new_line='')
                else:
                    # we are done here
                    break

    # add files to install list (no directories!)
    def add_files(self, base_path):

        for root, dirs, files in os.walk(base_path):

            for dir in dirs:
                sprint('.', new_line='')
                # TODO recursion not necessary here
                #self.add_files(join(root, dir))

            for file in files:
                sprint('#', new_line='')

                # remove matrix diff root path
                base_path = join(root, file)
                test = str(self.__task.matrix42_diff_dir + '/C/')
                base_path = base_path.replace(test, '')

                # construct a file install entry
                install_entry = '1:' + base_path + ','
                install_entry = install_entry + ' ' * (196-len(install_entry))
                install_entry = install_entry + 'C:/,'
                install_entry = install_entry + ' ' * (50-len('C:/'))
                install_entry = install_entry + 'CLIENT MACHINE,'
                install_entry = install_entry + ' ' * (34-len('C:/'))
                install_entry = install_entry + str(getsize(join(root, file)))
                self.__setup_inf.inf[si.Package.set_product][install_entry] = ''

    # create package directory
    def create_package_dir(self):
        # create basic package dir structure
        os.makedirs(self.__task.package_base_dir + '/' + self.__task.app_vendor + '/' + self.__task.app + '/' + self.__task.app_version + '/install')

    # save setup.inf
    def save_inf(self):
        with open(self.__task.package_base_dir + '/' + self.__task.app_vendor + '/' + self.__task.app + '/' + self.__task.app_version + '/install/Setup.inf', 'w') as file:
            
            inf = self.generate_inf()

            for entry in inf:
                file.write(entry + '\n')

    # copy all dirs and files from the Matrix42 Diff directory into target
    def copy_diff_data(self):
        base_dir = self.__task.matrix42_diff_dir + '/C'
        target_dir = self.__task.package_base_dir + '/' + self.__task.app_vendor + '/' + self.__task.app + '/' + self.__task.app_version

        # get all files in Diff/C only
        for root, dirs, files in os.walk(base_dir):
            for dir in dirs:
                shutil.copytree(src=str(base_dir + '/' + dir), dst=target_dir + '/' + dir)
                sprint('#', new_line='')

            # only the top directories are mandatory since we copy them recursively
            # so, just stop at the first traversal
            break

