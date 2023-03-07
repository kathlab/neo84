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
        # SET system environment variable
        # PATH a path entry to PATH system environment variable

        match = re.search('^\[|^;|^HK[CRLM]{2}|^#|^[0-9]{1}:|^SET|^PATH', key)
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

    # extract sys env reg adds in usable form
    def __extract_sys_env_variable(self, value):

        # TODO likely to refactor to something better designed
        result = {
            si.Sys_env_vars.env_name: '',
            si.Sys_env_vars.env_values: []
        }

        # TODO make customizable
        # filter all windows specific path entries
        win_filter_list = [
            '%SystemRoot%',
            '%SYSTEMROOT%',
            '[sS]{1,1}ystem32',
        ]

        match = re.match(r'^HKLM,"SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment","(.*)",[0-9a-fA-Fx]*,"(.*)"', value)
        if (match != None and len(match.groups()) == 2):
            result[si.Sys_env_vars.env_name] = match.groups()[0]

            temp = match.groups()[1].replace('"', '')
            
            for path in temp.split(';'):
                win_sys_env_found = False

                # find any win sys envs by regex filter
                for entry in win_filter_list:
                    filter_match = re.search(entry, path)
                    if (filter_match != None):
                        win_sys_env_found = True
                        sprint('W', '')
                        break

                # ignore win sys envs
                if (win_sys_env_found):
                    continue

                result [si.Sys_env_vars.env_values].append(path)
        
        return result

    # add a system environment variable to setup.inf
    def __add_sys_env_variables(self, value):
        entry = ''

        # TODO likely to refactor sys env "struct"
        # TODO likely to refactor 'Path' and 'SET' etc.
        # distinct between simple (single) and PATH (multiple)
        if (value[si.Sys_env_vars.env_name] == 'Path'):
            # could be multiple PATH entries
            for path in value[si.Sys_env_vars.env_values]:
                entry = 'PATH >' + path
                
                # add entry to Autoexec.bat:Product
                self.setup_inf.inf[si.Package.autoexec_bat_product][entry] = ''
        else:
            # just one entry, could be anything including a path
            entry = 'SET ' + value[si.Sys_env_vars.env_name] + '=' + value[si.Sys_env_vars.env_values][0]

            # add entry to Autoexec.bat:Product
            self.setup_inf.inf[si.Package.autoexec_bat_product][entry] = ''


    # check if a HKLM line contains a sys env variable
    # we need to filter them out of reg adds
    # otherwise we overwrite sys env variable which is bad
    def __is_sys_env(self, value):
        match = re.search(r'^HKLM,"SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment".*', value)
        if (match != None):
            return True
        
        return False

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

        for package_section in range(0, 22):
            entries = self.__setup_inf.inf[package_section]
            inf.append('')
            for key,value in entries.items():
                inf.append(self.__build_inf_line(key, value))

        return inf
    
    # add all registry additions from Diff.inf
    def add_diff_reg(self, file_name):
        
        # TODO bad things happen with windows encoded text file opened as UTF-8
        with open(file_name, mode='r', encoding='ISO-8859-1') as file:
            
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

                # filter and extract sys env reg additions
                if (self.__is_sys_env(line)):
                    sys_env_variable = self.__extract_sys_env_variable(line)
                    self.__add_sys_env_variables(sys_env_variable)
                    continue

                match = re.search('^HK[CRLMU]{2},', line)
                if (match != None):
                    filterlist_found = False

                    # TODO generalize filter
                    # check if we have to apply filterlist expression
                    if (self.task.use_reg_filterlist):
                       
                        for rx in self.task.reg_filterlist:
                            match = re.search(rx, line)
                            if (match != None):
                                # found entry, done and proceed
                                filterlist_found = True
                                break

                        # skip to next line if entry is not in filterlist
                        if (filterlist_found == False):
                            continue

                    # add to list but remove line breaks
                    self.setup_inf.inf[si.Package.reg_product][line.replace('\n', '')] = ''
                    
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
                filterlist_found = False
                
                sprint('#', new_line='')

                # remove matrix diff root path
                base_path = join(root, file)
                base_path = base_path.replace(str(self.task.matrix42_diff_dir + '/C/'), '')

                # TODO make filterlist filter more general
                # apply filterlist
                if (self.task.use_dir_file_filterlist):
                    for entry in self.task.dir_file_filterlist:
                        match = re.search(entry, base_path)

                        if (match != None):
                            filterlist_found = True
                            break
                
                    # skip file or directory if not found via filterlist
                    if (filterlist_found == False):
                        continue

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

    # save setup.inf (in ISO-8859-1 encoding!)
    def save_inf(self):
        with open(self.__task.package_base_dir + '/' + self.__task.app_vendor + '/' + self.__task.app + '/' + self.__task.app_version + '/install/Setup.inf', mode='w', encoding='ISO-8859-1') as file:
            
            inf = self.generate_inf()

            for entry in inf:
                file.write(entry + '\n')

    # copy all dirs and files from the Matrix42 Diff directory into target (no white list)
    def copy_diff_data(self):
        base_dir = self.__task.matrix42_diff_dir + '/C'
        target_dir = self.__task.package_base_dir + '/' + self.__task.app_vendor + '/' + self.__task.app + '/' + self.__task.app_version

        # get all files in Diff/C only
        for root, dirs, files in os.walk(base_dir):
            
            for dir in dirs:
                shutil.copytree(src=str(base_dir + '/' + dir), dst=str(target_dir + '/' + dir))
                sprint('#', new_line='')

            # only the top directories are mandatory since we copy them recursively
            # so, just stop at the first traversal
            break

    # copy dirs and files according to white lists
    def copy_diff_filterlist_data(self):
        base_dir = self.__task.matrix42_diff_dir + '/C'
        target_dir = self.__task.package_base_dir + '/' + self.__task.app_vendor + '/' + self.__task.app + '/' + self.__task.app_version

        # copy everything according to filterlists
        for root, dirs, files in os.walk(base_dir):

            for dir in dirs:
                sprint('.', new_line='')

            for file in files:
                filterlist_found = False
                source_path = join(root, file)

                # replace matrix diff root path with target path
                target_path = source_path.replace(str(self.task.matrix42_diff_dir + '/C'), target_dir)

                # TODO make filterlist filter more general
                # apply filterlist
                if (self.task.use_dir_file_filterlist):
                    for entry in self.task.dir_file_filterlist:
                        match = re.search(entry, source_path)

                        if (match != None):
                            filterlist_found = True
                            break
                
                    # skip file or directory if not found via filterlist
                    if (filterlist_found == False):
                        continue

                # create target directory, ignore if dir exists
                target_head_path = os.path.dirname(target_path)
                try:
                    os.makedirs(target_head_path)
                except FileExistsError as ex:
                    sprint('!', new_line='')

                shutil.copy(source_path, target_path)
                sprint('#', new_line='')

    # add all system environment entries from Diff.inf
    # theses are "hidden" inside registry additions
    def get_sys_env_entries(self, file_name):
        
        # TODO bad things happen with windows encoded text file opened as UTF-8
        with open(file_name, mode='r', encoding='ISO-8859-1') as file:
            
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
                match = re.search('^HK[CRLMU]{2},', line)
                if (match != None):
                    filterlist_found = False

                    # TODO generalize filter
                    # check if we have to apply filterlist expression
                    if (self.task.use_reg_filterlist):
                       
                        for rx in self.task.reg_filterlist:
                            match = re.search(rx, line)
                            if (match != None):
                                # found entry, done and proceed
                                filterlist_found = True
                                break

                        # skip to next line if entry is not in filterlist
                        if (filterlist_found == False):
                            continue

                    # add to list but remove line breaks
                    self.setup_inf.inf[si.Package.reg_product][line.replace('\n', '')] = ''
                    
                    sprint('#', new_line='')
                else:
                    # we are done here
                    break