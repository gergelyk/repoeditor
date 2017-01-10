# repoeditor

Editor of small and medium size repositories of Npackd package manager.


## Linux Users

### Installation

Linux users are intended to simply copy source files to the destination directory. Python3 with PyQt4 module must me installed in the system.

### Running

Simply invoke following command:

```
python repoeditor.py
```

## Windows Users

### Installation

Windows users are encouraged to use installer which installs compiled version of the application in their system.

Alternatively repoeditor can be installed from the official repository using [npackd](http://npackd.appspot.com/) package manager.

### Running

Simply start repoeditor.exe, or use shortcut in your Start Menu.

### Building

The application requires [Python3](https://www.continuum.io/why-anaconda) with [PyQt4](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4) module installed.

In addition you need to install `dodo` and `PyInstaller` modules. This can be done by invoking:

```
pip install dodo
pip install pyinstaller
```
Finally Inno Setup needs to be installed in order to build the installer.

After preparing your environment as described above

1. Update `version.txt` file with the version of repoeditor that you would like to build.

2. In the top directory invoke:
```
doit installer
```

Alternatively you can invoke:
```
doit install
```

if you would like the tool chain to immediately install the application after building it. Installation directory can be specified in dodo.py

Finally
```
doit clean
```

uninstalls the application and cleans working directory.

Following software versions have been used for building version 1.1.3:

* Python 3.5.2 :: Anaconda 4.2.0 (64-bit)
* PyInstaller 3.2
* PyQt4-4.11.4-cp35-none-win_amd64
* Inno Setup 5.5.9
