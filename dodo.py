INSTALLATION_DIR="C:\\Programs\\npackd-repoeditor"

def get_version():
    with open('version.txt') as fh:
        version = fh.read().strip()
    return version

def task_version():
    def create_version_file():
        version = get_version()
        with open('src\\repoeditor\\version.py', 'w') as fh:
            fh.write('APP_VERSION = "' + version + '"')

    return {
        'actions': [create_version_file],
		'file_dep': ["version.txt"],
		'targets': ["src\\repoeditor\\version.py"],
		'clean': True,
        }

def task_executable():

    return {
        'actions': ["pyinstaller -w -F -i res/repoeditor.ico src/repoeditor.py"],
		'file_dep': ["src\\repoeditor\\version.py"],
		'targets': ["dist\\repoeditor.exe"],
		'clean': ["rmdir /Q /S dist", "rmdir /Q /S build", "del repoeditor.spec"],
        }

def task_installer():

    return {
        'actions': ["iscc installer.iss"],
		'file_dep': ["dist\\repoeditor.exe"],
		'targets': ["installer", "installer\\npackd-repoeditor-" + get_version() + "-setup.exe"],
		'clean': True,
        }
		
def task_install():

    return {
        'actions': ["installer\\npackd-repoeditor-" + get_version() + "-setup.exe /VERYSILENT /SUPPRESSMSGBOXES /NORESTART /DIR=" + INSTALLATION_DIR],
		'file_dep': ["installer\\npackd-repoeditor-" + get_version() + "-setup.exe"],
		'clean': [INSTALLATION_DIR + "\\unins000.exe /VERYSILENT /SUPPRESSMSGBOXES /NORESTART"],
        }
