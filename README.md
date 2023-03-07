```
                   _____   ___ 
                  |  _  | /   |
  _ __   ___  ___  \ V / / /| |
 | '_ \ / _ \/ _ \ / _ \/ /_| |
 | | | |  __/ (_) | |_| \___  |
 |_| |_|\___|\___/\_____/   |_/
 Package builder for Matrix42 🎁
```

__Please note:__ This app is under development, buggy and may crash anything which comes in contact with and it drinks away your coffee! neo84 is also not affiliated with Matrix42 AG by any means. It does not use any components nor secret wisdom from the Matrix42 software.

neo84 is an incomplete Matrix42 compatible package creator. There's no way to get every use case covered since some parts are reverse engineered (due to unavailable technical documentation), others are from freely available documentation and examples. I created this for my specific needs and others may also like it. I work mostly on macOS and Linux-based machines, so having a package creation environment for Matrix42 on non-Windows makes my life a lot easier.

__It is mandatory to look into the generated results and make sane changes AND PEFORM TESTS! If you brick your computer installations, please don't blame this app ;)__

To currently create packages, a Diff directory created by the _Matrix 42 Package Wizard_ is required.

neo84 should work fine for:

* build packages on linux or dockerized environments
* create packages from a system diff

What I have planned to implement and thus mostly __NOT IMPLEMENTED YET__:

* cleanup code []
* add filter lists for registry and files [__IMPLEMENTED__]
* add system environment variables processing [__IMPLEMENTED__]
* generate simple packages from scratch to... []
    * ...add system environment variables (PATH, etc.) []
    * ...copy files on targets without having any setup.exe on hands []
    * ...perform unattended installs []
    * ...maybe MSI installs []

How to create Matrix 42 package with neo84:
---

1. Run a system diff install with Matrix 42 Package Wizard
2. Copy Diff directory on whatever machine you like to work on
3. Inspect Diff.inf and remove all files and directories which do not belong to the app you want to package.
4. Create a task file (check out the examples in tasks/)
5. Run neo84 task
6. __REVIEW__ Setup.inf
7. __TEST__ package extensively

Common pitfalls in creating Matrix 42 packages
---

It's easy to create a feral package which just destroys your target machine. Using a fresh VM for testing out packages is the preferred and safest way. However some pitfalls are mandatory to avoid:

__1. Install package. No audition nor tests.__

```
"If one like to blow up a computer installation, just install without package sanity check."
```
Listen to the words of wisdom. Audition and testing is mandatory, not an option.

__2. Accidentically set system environment variables__

This can be fatal especially if the package gets uninstalled. The installation looks fine but chaos breaks loose upon uninstallation. Everything __set__ is getting __unset__! This can easily clear out your complete system path etc. Just set what is specific to the application itself.

__3. Install things which do not belong to your app__

Also fatal if you install any windows update stuff which compromises the machine installation. Keep an eye on registry entries. And make use of filter lists to get rid of any unwanted data when running a neo84 task. Less is more.

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
2. Dev Containers: Reopen in Container
3. Install VS Code extensions as needed