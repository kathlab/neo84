from enum import IntEnum

# setup.inf documentation
# @see https://helpfiles.matrix42-web.de/2020_EN/M42_WebDocu.htm#WM/PWM/SWM/SETUP/Referenz/Sections/SETUP_Section_01_INF.htm?TocPath=Unified%2520Endpoint%2520Management%257CEmpirum%257C-%2520Client%2520Software%2520-%257CSETUP%257CTechnical%2520Reference%257CStructure%2520of%2520the%2520File%2520Setup.inf%257C_____0
# @see https://www.itnator.net/matrix42-empirum-setup-inf-beispiel/

# setup inf header
class Package(IntEnum):
    meta_data = 0, # mostly static, version info, etc.
    variables = 1, # define variables for ???
    setup = 2, # setup settings
    requirements = 3, # ???
    m42_app_constants = 4, # requires modification
    m42_install_de = 5, # doesn't change, don't care
    m42_install_en = 6, # doesn't change, don't care
    m42_user_de = 7, # doesn't change, don't care
    m42_user_en = 8, # doesn't change, don't care
    environment = 9, # doesn't change, don't care
    encryption = 10, # unused, don't care
    disks = 11, # doesn't change, don't care
    options = 12, # doesn't change, don't care
    installer = 13, # setup installer files, don't care
    product = 14, # doesn't change, don't care
    set_product = 15, # file install list
    reg_uninstall = 16, # doesn't change, don't care
    reg_product = 17, # registry additions list
    ini_product = 18, # doesn't change, don't care
    security_product = 19, # doesn't change, don't care
    shell_product = 20, # start menu links, etc.
    autoexec_bat_product = 21, # system environment variables

class Setup_inf():

    def __init__(self):
        
        self.__inf = []

        # package header
        self.__meta_data = {
            '[SetupInfo]': '',
            'Author': 'Mr. Nobody', # your name
            'CreationDate': '', # DD.MM.YYYY
            'InventoryID': '', # ???
            'Description': '', # comment
            'Method': 'neo84', # package creation method [MSI, ???]
            'Tested on': 'Windows 10', # OS, eg. Windows 10
            'Dependencies': '', # don't care
            'Command line options': '', # don't care
            'Last Change': '', # a date
            'Build': '0', # int build number [0..n]
        }

        self.__inf.append(self.__meta_data)

        # variables
        self.__variables = {
            '[VarDefInfo]': '',
        }

        self.__inf.append(self.__variables)

        # setup
        self.__setup = {
            '[Setup]': '',
            'Version': '14.2', # default 14.2
            'ShowCaptions': '1', # default=1
            'BlockInput': '0', # disable user inputs, default=0
            'Platform': '*' # default=*
        }
        
        self.__inf.append(self.__setup)

        # requirements
        self.__requirements = {
            '[Requirements]': ''
        }

        self.__inf.append(self.__requirements)

        # application
        self.__application = {
            '[Application]': '',
            'ProductName': '{ProductName}', # mandatory
            'DeveloperName': '{DeveloperName}', # mandatory
            'Version': '{Version}', # mandatory
            'Revision': '{Revision}', # default=0
            'SetupName': '%ProductName% %Version% %SetupWizard%',
            'Text1': '"%ProductName% %Version%",         Arial,           30, , 2170F3, 4,    , LEFT BOLD ITALIC',
            'Text2': '"%DeveloperName%",                 Arial,           24, , 2170F3, 4,    , LEFT BOLD ITALIC',
            'Text8': '"%Company%",                       Arial,           18, , 2170F3, 4,  10, RIGHT BOLD ITALIC',
            'Text9': '"%InstallationFor% %WindowsUser%", Arial,           16, , 2170F3, 4, -18, BOTTOM ITALIC LEFT',
            'BackgroundColor': 'EFEFEF,000000',
            'CopyDialogRect': '0%, 0%, 100%, 100%, HCENTER VCENTER',
            '; Register all installations in common registry key': '',
            'UserKeyName': r'$Matrix42Packages$\%DeveloperName%\%ProductName%',
            'MachineKeyName': r'$Matrix42Packages$\%DeveloperName%\%ProductName%\%Version%',
            'UninstallKeyName': r'Matrix42 - %DeveloperName% %ProductName% %Version%',
            'UninstallDisplayName': r'Matrix42 - %DeveloperName% %ProductName% %Version%',
            'UninstallString': '%ReinstallString% /U',
            'ReinstallString': r'"%CommonSetupDir%\Setup.exe' '%App%\%SetupInfDir%\Setup.inf"',
            '; UninstallDisplayIcon': r'"%ApplicationDir%\%SetupInfDir%\Setup.ico",0',
            'UninstallOptions': 'NOREMOVE NOREPAIR NOMODIFY',
            'ReinstallMode': '1',
            'SrcDir': '..',
            'ApplicationDir': r'%ProgramFilesDir%\%ProductName%',
            'SetupInfDir': 'Install',
            'DataDir': '%Personal%',
            'AskUninstallOld': '1',
            'ShellLinks': '1',
            'CommonShellLinks': '0',
            'CreateUnresolvableShellLinks': '1',
            'UseStringSection': 'Strings:09', # lang
            'UseSysStringSection': 'SysStrings:09', # lang
            'DateWarning': '1',
            'SizeWarning': '0',
            'Reboot': '0',
            'PreventExternalReboot': '1',
            'StartServicesOnReboot': '0',
            'CallTimeOut': '3600',
            'AbortAfterCallTimeOut': '1',
            'DisableCancelButton': '1',
            'ShowEndMessage': '1',
            'EndMessage': r'%EndMessageDesc%',
        }

        self.__inf.append(self.__application)

        self.__m42_install_de = {
            '[Strings:07]': '',
            'Disk1': 'Installationsmedium 1',
            'EndMessageDesc': 'Die Installation wurde erfolgreich abgeschlossen!',
            'ErrorLogMessage': 'Die Installation/Deinstallation wurde mit einer Fehlermeldung abgebrochen!',
            'InstallationFor': 'Installation fuer:',
            'InstallerDesc': 'Dienstprogramm zum Installieren einzelner Komponenten.',
            'InstallerName': 'Installationsprogramm',
            'SetupWizard': 'Installations-Assistent',
            'Uninstallation': 'deinstallieren',
        }

        self.__inf.append(self.__m42_install_de)

        self.__m42_install_en = {
            '[Strings:09]': '',
            'Disk1': 'Installation media 1',
            'EndMessageDesc': 'Installation was completed successfully!',
            'ErrorLogMessage': 'The installation/uninstallation aborted with an error message!',
            'InstallationFor': 'Installation for:',
            'InstallerDesc': 'Service program to install single components.',
            'InstallerName': 'Setup program',
            'SetupWizard': 'Installation Wizard',
            'Uninstallation': 'Uninstallation'
        }

        self.__inf.append(self.__m42_install_en)

        self.__m42_user_de = {
            '[SysStrings:07]': '',
            'Users': 'Benutzer',
        }

        self.__inf.append(self.__m42_user_de)

        self.__m42_user_en = {
            '[SysStrings:09]': '',
            'Users': 'Users',
        }

        self.__inf.append(self.__m42_user_en)

        self.__environment = {
            '[Environment]': '',
            'CommonSetupDir': r'%CommonFilesDir%\Setup%SetupBits%',
            'V_MachineValuesPath': r'\\%EmpirumServer%\Values$\MachineValues\%DomainName%',
            'V_UserValuesPath': r'%HKLM,"Software\matrix42\Software Depot","HomeServer"%\Values$\UserValues\%UserDomain%',
        }

        self.__inf.append(self.__environment)

        self.__encryption = {
            '[Encryption]': '',
        }
        
        self.__inf.append(self.__encryption)

        self.__disks = {
            '[Disks]': '',
            '1': '%Disk1%'
        }

        self.__inf.append(self.__disks)

        self.__options = {
            '[Options]': '',
            'Installer': '%InstallerName%, COPYALWAYS, Installer, "%InstallerDesc%"',
            'Product': '%ProductName%,   COPYALWAYS, Product,   "%ProductDesc%"',
        }

        self.__inf.append(self.__options)

        self.__installer = {
            '[Installer]': '',
            r'1:..\..\..\..\User\Setup.exe,          %CommonSetupDir%, OPTIONAL USEFILENAME DIRECTORY NOSIZEWARNING SETUP, 0': '',
            r'1:..\..\..\..\User\SetupDeu.chm,       %CommonSetupDir%, OPTIONAL USEFILENAME DIRECTORY NOSIZEWARNING SETUP, 0': '',
            r'1:..\..\..\..\User\SetupEnu.chm,       %CommonSetupDir%, OPTIONAL USEFILENAME DIRECTORY NOSIZEWARNING SETUP, 0': '',
            r'1:%Temp%\Setup64.exe,                  %CommonSetupDir%\Setup.exe, OPTIONAL ALWAYS NOSIZEWARNING SETUP WINDOWS64,     0': '',
            r'1:..\..\..\..\User\Setup64.exe,        %CommonSetupDir%\Setup.exe, OPTIONAL ALWAYS NOSIZEWARNING SETUP WINDOWS64,     0': '',
            r'1:%SetupInfDir%\Setup.inf,                             , ALWAYS,                                             0': '',
            r'; 1:%SetupInfDir%\Setup.ico,                             , NORMAL,                                           0,: '''
            r'; 1:%SetupInfDir%\Logo.bmp,                              , NORMAL,      ': '',
        }

        self.__inf.append(self.__installer)

        self.__product = {
            '[Product]': '',

            # activate sections to run installer actions
            # leave as-is and keep sections just empty
            '#Set:Product': '',
            '#Reg:OnUninstallProduct, DELETE': '',
            '#Reg:Product': '',
            '#Ini:Product': '',
            '#Security:Product': '',
            '#Autoexec.bat:Product': '',
        }

        self.__inf.append(self.__product)

        self.__set_product = {
            '[Set:Product]': '',
            '; 1:, %App%, CREATE DIRECTORY CASCADED, 0': ''

            # both paths are concatenated to build a absolute path. just the first part of the path is different.
            # 1:RELATIVE_PATH, ABSOLUTE_PATH_START_AT_C_DRIVE, INSTALL_TARGET, SIZE_IN_BYTES 

            # install in %ProgramFilesDir%
            # 1:NVIDIA Corporation\PhysX\Common\cudart32_65.dll,                                                                                                                                                  %ProgramFilesDir%,                                CLIENT MACHINE,                     254672

            # install in C:
            # 1:Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.6\version.json,                                                                                                                               C:\,                                              CLIENT MACHINE,                       2817
        }

        self.__inf.append(self.__set_product)

        self.__reg_uninstall = {
            '[Reg:OnUninstallProduct]': '',
        }

        self.__inf.append(self.__reg_uninstall)

        self.__reg_product = {
            '[Reg:Product]': '',
        }

        self.__inf.append(self.__reg_product)

        self.__ini_product = {
            '[Ini:Product]': '',
        }

        self.__inf.append(self.__ini_product)

        self.__security_product = {
            '[Security:Product]': '',
        }

        self.__inf.append(self.__security_product)

        self.__shell_product = {
            '[Shell:Product]': '',
        }

        self.__inf.append(self.__shell_product)

        self.__autoexec_bat_product = {
            '[Autoexec.bat:Product]': '',

            # set a new variable in system environment
            # SET MY_VARIABLE_NAME=WHATEVER
            # SET CUDA_PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.6

            # add path to PATH variables
            # PATH >MY_PATH
            # PATH >C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.6\bin
        }

        self.__inf.append(self.__autoexec_bat_product)
    
    @property
    def inf(self):
        return self.__inf

    @inf.setter
    def inf(self, value):
        self.__inf = value