from neo84_print import sprint
from os.path import join, getsize
import neo84_filter as filter
import neo84_sysenv as sysenv
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

    def __is_in_filter(self, filter, value):
        found = False

        for entry in filter:
            filter_match = re.search(entry, value)
            if (filter_match != None):
                found = True
                sprint('F', '')
                break

        return found

    # extract sys env reg adds in usable form
    def __extract_sys_env_variable(self, value):
        sysenv_vars = sysenv.Sysenv_var()

        # filter all windows specific path entries
        win_filter_list = filter.Filter_list(filter.WIN_SYSENV_FILTER)

        match = re.match(r'^HKLM,"SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment","(.*)",[0-9a-fA-Fx]*,"(.*)"', value)
        if (match != None and len(match.groups()) == 2):
            sysenv_vars.name = match.groups()[0]

            temp = match.groups()[1].replace('"', '')
            
            for path in temp.split(';'):

                # ignore win sysenv vars
                if (self.__is_in_filter(win_filter_list.filter, path)):
                    continue

                sysenv_vars.values.append(path)
        
        return sysenv_vars

    # add a system environment variable to setup.inf
    def __add_sys_env_variables(self, value: sysenv.Sysenv_var):
        entry = ''

        # TODO likely to refactor 'Path' and 'SET' etc.
        # distinct between simple (single) and PATH (multiple)
        if (value.name == 'Path'):
            # could be multiple PATH entries
            for path in value.values:
                entry = 'PATH >' + path
                
                # add entry to Autoexec.bat:Product
                self.setup_inf.inf[si.Package.autoexec_bat_product][entry] = ''
        else:
            # just one entry, could be anything including a path
            entry = 'SET ' + value.name + '=' + value.values[0]

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
        self.__setup_inf.inf[si.Package.meta_data]['Author'] = self.task.author
        self.__setup_inf.inf[si.Package.meta_data]['CreationDate'] = self.task.date
        self.__setup_inf.inf[si.Package.meta_data]['Tested on'] = self.task.os
        self.__setup_inf.inf[si.Package.meta_data]['Build'] = self.task.build
        self.__setup_inf.inf[si.Package.meta_data]['Description'] = self.task.description

        for package_section in range(0, 22):
            entries = self.setup_inf.inf[package_section]
            inf.append('')
            for key,value in entries.items():
                inf.append(self.__build_inf_line(key, value))

        return inf
    
    # add all registry additions from Diff.inf
    def add_diff_reg(self, file_name):
        
        # bad things happen with windows encoded text file opened as UTF-8
        with open(file_name, mode='r', encoding='ISO-8859-1') as file:
            
            # TODO line_found refactor to filter_list
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
                    # check if we have to apply filterlist expression
                    if (self.task.use_reg_filterlist):
                        reg_filter = filter.Filter_list(self.task.reg_filterlist)

                        # skip to next line if entry is not in filterlist
                        if (self.__is_in_filter(reg_filter.filter, line) == False):
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

            for file in files:
                sprint('#', new_line='')

                # remove matrix diff root path
                base_path = join(root, file)
                base_path = base_path.replace(str(self.task.matrix42_diff_dir + '/C/'), '')

                dirfile_filter = filter.Filter_list(self.task.dir_file_filterlist)

                # skip file or directory if not found via filterlist
                if (self.__is_in_filter(dirfile_filter.filter, base_path) == False):
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
                sprint('#', '')

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
                source_path = join(root, file)

                # replace matrix diff root path with target path
                target_path = source_path.replace(str(self.task.matrix42_diff_dir + '/C'), target_dir)

                dirfile_filter = filter.Filter_list(self.task.dir_file_filterlist)

                # skip file or directory if not found via filterlist
                if (self.__is_in_filter(dirfile_filter.filter, source_path) == False):
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
        
        # bad things happen with windows encoded text file opened as UTF-8
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
                    # check if we have to apply filterlist expression
                    if (self.task.use_reg_filterlist):
                        reg_filter = filter.Filter_list(self.task.reg_filterlist)

                        # skip to next line if entry is not in filterlist
                        if (self.__is_in_filter(reg_filter.filter, line) == False):
                            continue

                    # add to list but remove line breaks
                    self.setup_inf.inf[si.Package.reg_product][line.replace('\n', '')] = ''
                    
                    sprint('#', new_line='')
                else:
                    # we are done here
                    break