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
            'use_reg_whitelist': False,
            'use_dir_file_whitelist': False,
            'reg_whitelist:': [],
            'dir_whitelist:': [],
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
    def reg_whitelist(self):
        return self.yaml['reg_whitelist']
    
    @property
    def dir_file_whitelist(self):
        return self.yaml['dir_file_whitelist']

    @property
    def use_reg_whitelist(self):
        return self.yaml['use_reg_whitelist']

    @property
    def use_dir_file_whitelist(self):
        return self.yaml['use_dir_file_whitelist']

    def load_from_file(self, file_name):
        with open(file_name, 'r') as file:
            self.yaml = yaml.safe_load(file)
