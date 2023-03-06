from enum import IntEnum
import io
import yaml

class Neo84_task():

    def __init__(self):
        self.yaml = {
            'app': '',
            'author': '',
            'date': '',
            'os': '',
            'build': '',
            'matrix42_diff_dir': '', # path to Matrix42 temp data including Diff/
            'app_vendor': '',
            'app_version': '',
            'package_base_dir': '',
            'use_reg_filterlist': False,
            'use_dir_file_filterlist': False,
            'reg_filterlist:': [],
            'dir_filterlist:': [],
        }

    @property
    def app(self):
        return self.yaml['app']

    @property
    def author(self):
        return self.yaml['author']

    @property
    def date(self):
        return self.yaml['date']
    
    @property
    def os(self):
        return self.yaml['os']
    
    @property
    def build(self):
        return self.yaml['build']
        
    @property
    def matrix42_diff_dir(self):
        return self.yaml['matrix42_diff_dir']

    @property
    def app_vendor(self):
        return self.yaml['app_vendor']

    @property
    def app_version(self):
        return self.yaml['app_version']

    @property
    def package_base_dir(self):
        return self.yaml['package_base_dir']

    @property
    def reg_filterlist(self):
        return self.yaml['reg_filterlist']
    
    @property
    def dir_file_filterlist(self):
        return self.yaml['dir_file_filterlist']

    @property
    def use_reg_filterlist(self):
        return self.yaml['use_reg_filterlist']

    @property
    def use_dir_file_filterlist(self):
        return self.yaml['use_dir_file_filterlist']

    def load_from_file(self, file_name):
        with open(file_name, 'r') as file:
            self.yaml = yaml.safe_load(file)
