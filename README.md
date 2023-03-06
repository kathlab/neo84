```
                   _____   ___ 
                  |  _  | /   |
  _ __   ___  ___  \ V / / /| |
 | '_ \ / _ \/ _ \ / _ \/ /_| |
 | | | |  __/ (_) | |_| \___  |
 |_| |_|\___|\___/\_____/   |_/
 Package builder for Matrix42
```

__Please note:__ This app is under development, buggy and may crash anything which comes in contact with and it drinks away your coffee! neo84 is also not affiliated with Matrix42 AG by any means. It does not use any components from the Matrix42 software.

neo84 is an incomplete Matrix42 compatible package creator. There's no way to get every use case covered since some parts are reverse engineered (due to unavailable technical documentation), others are from freely available documentation and examples. I created this for my specific needs and others may also like it. I work mostly on macOS and Linux-based machines, so having a package creation environment for Matrix42 on non-Windows makes my life a lot easier.

It is mandatory to look into the generated results and make sane changes AND PEFORM TESTS! __If you brick your computer installations, please don't blame this app ;)__

To create packages, a Diff directory created by the _Matrix 42 Package Wizard_ is required.

neo84 should work fine for:

* build packages on linux or dockerized environments
* create packages from a system diff (__under current development!__)

What I have planned to implement and thus mostly __NOT IMPLEMENTED YET__:

* add filter lists for registry and files [__IMPLEMENTED__]
* add system environment variables processing []
* generate simple packages from scratch to... []
    * ...add system environment variables (PATH, etc.) []
    * ...copy files on targets without having any setup.exe on hands []
    * ...perform unattended installs []
    * ...maybe MSI installs []

Create Matrix42 package with neo84:
---

1. Create a file MY_TASK.yaml

```
# name of the application
app: "Anaconda"

# name of the vendor
app_vendor: "Anaconda3"

# application version
app_version: "2022.10"

# location of the Matrix42 Diff directory
matrix42_diff_dir: "C:/Temp/Diff"

# location where to store the package
package_base_dir: "targets"

# your name
author: "Mrs. Curious"

# build date
date: "24.02.2023"

# build os
os: "Windows 10"

# build number
build: "0"

# filterlist toggle
use_reg_filterlist: True
use_dir_file_filterlist: True

# filterlists may contain regular expressions :)
# however, don't mix around "" and '' in strings - yaml won't like that
# instead, create a more general regex

# registry filterlist
reg_filterlist:
  - 'HKCU.*Anaconda3.*'

# dir and file filterlist
# empty directories are NOT copied!
dir_file_filterlist:
  - 'ProgramData/Anaconda3'
  - 'ProgramData/Microsoft/Windows/Start Menu/Programs/Anaconda3 \(64-bit\)'
  - 'Users/All Users/Anaconda3'
  - 'Users/All Users/Microsoft/Windows/Start Menu/Programs/Anaconda3 \(64-bit\)'
  - 'Users/Public/Documentws/Python Scripts'
```

2. Run neo84 to create package

```
$ python neo84.py MY_TASK.yaml
```

3. __REVIEW__ Setup.inf
4. __TEST__ package

Build docker image:
---

```
$ docker build -f Dockerfile -t local/neo84:latest .
```

Create and run docker container:
---

```
$ docker compose up -d
```

Run VS Code inside docker container
---

1. Open VS Code workspace
2. (optional) Add ports forwarding of 8888 and 8889 in VS Code (for Juypter Notebook web app)
3. Dev Containers: Reopen in Container
4. Install VS Code extensions as needed