#######################################################################################
#                                                                                     #
# This file is an equivalent of Makefile. In order to use it, you need to have Python #
# installed together with 'doit' modle. For more information check http://pydoit.org/ #
#                                                                                     #
# Syntax:                                                                             #
# doit TARGETNAME                                                                     #
#                                                                                     #
######################################################################################

INSTALLATION_DIR="C:\\Programs\\npackd-repoeditor"

def get_version():
    """Reads version.txt file to obtain version number of the software to be build
    """
    with open('version.txt') as fh:
        version = fh.read().strip()
    return version

def task_version():
    """Creates version.py file based on version.txt
    """
    def create_version_file():
        version = get_version()
        with open('src\\lib\\version.py', 'w') as fh:
            fh.write('APP_VERSION = "' + version + '"')

    return {
        'actions': [create_version_file],
		'file_dep': ["version.txt"],
		'targets': ["src\\lib\\version.py"],
		'clean': True,
        }

def task_executable():
    """Compiles executable. It can be found in 'dist' directory.
    """

    return {
        'actions': ["pyinstaller -w -F -i res/repoeditor.ico src/repoeditor.py"],
		'file_dep': ["src\\lib\\version.py"],
		'targets': ["dist\\repoeditor.exe"],
		'clean': ["rmdir /Q /S dist", "rmdir /Q /S build", "del repoeditor.spec"],
        }

def task_installer():
    """Builds installer package which contains executable and other resource files
    """

    return {
        'actions': ["iscc installer.iss"],
		'file_dep': ["dist\\repoeditor.exe"],
		'targets': ["installer", "installer\\npackd-repoeditor-" + get_version() + "-setup.exe"],
		'clean': True,
        }
		
def task_install():
    """Installs software in the operating system
    """    

    return {
        'actions': ["installer\\npackd-repoeditor-" + get_version() + "-setup.exe /VERYSILENT /SUPPRESSMSGBOXES /NORESTART /DIR=" + INSTALLATION_DIR],
		'file_dep': ["installer\\npackd-repoeditor-" + get_version() + "-setup.exe"],
		'clean': [INSTALLATION_DIR + "\\unins000.exe /VERYSILENT /SUPPRESSMSGBOXES /NORESTART"],
        }

