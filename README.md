# repoeditor
Editor of small and medium size repositories of Npackd package manager.

## Installation
The application requires Python3 with PyQt4 module installed.

I assume that Linux users know what to do.

Windows users are encouraged to accomplish following steps:

1. Install Python3 interpreter. You can download the installer here:
  https://www.python.org/downloads/windows/

  It's easier however to use npackd - which I guess you are interested in. Install either org.python.Python package if you are using 32-bit platform or org.python.Python64 package if you are using 64-bit platform.

2. Install setuptools for Python. If you used one of the packages mentioned above, your setuptools are already installed.

3. Associate .py file extension which Python interpreter which doesn't show console window. Open console and type:
  ```
  assoc .py=Python.NoConFile
  ftype Python.NoConFile="C:\WINDOWS\pyw.exe" "%1" %*
  ```
  It may also be necessary to double click on the script and select Python interpreter as default application used for opening this file.

4. Add .py file extension to system variable PATHEXT. This will let you call Python scripts without extensions, directly in terminal, as they were executables.

5. Install PyQt4 package for Python. You may decide to compile it from source, or download precompiled version from here:
  http://www.lfd.uci.edu/~gohlke/pythonlibs/PyQt4-****.whl

  Select package relevant to architecture of your platform and to version of your Python interpreter. Version of Python can be checked by invoking
  ```
  Python -V
  ```
  After downloading package go to command line and invoke:
  ```
  pip install PyQt4-****.whl
  ```
  **WARNING: There are some (hopefully) temporary problems with Python 3.5 and Qt4. Please use Python 3.4 instead.**

## Usage
To start repoeditor simply double click repoeditor.py file, or go to console
and invoke:
```
repoeditor
```

## Notes
Your browser may not display XML file as expected until you copy `summary.xls`
file to the same directory where XML file is. `summary.xls` can be found in
`<repoeditor>/templates` directory. If you don't want to use such file, remove:

`<?xml-stylesheet type="text/xsl" href="summary.xsl"?>`

line in `<repoeditor>/templates/header.xml` and regenerate your XML file.
