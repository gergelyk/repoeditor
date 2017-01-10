import sys
import os
import xml.etree.ElementTree as ET
import webbrowser
from functools import partial
from PyQt4.QtGui import QMainWindow, QDesktopWidget, QAction, QActionGroup, QIcon, QMessageBox, QWidget
from PyQt4.QtGui import QSizePolicy
from lib.xmleditor import XmlEditor
from lib.feedbacks import *
from lib.version import APP_VERSION

class Gui(QMainWindow):
    """Main window of Qt application.
    """
    
    # Constant dictionary which links menus with feedback functions
    dynamic_menus = {}
    
    # Allows to change text in text editor without calling relevant
    # feedback function
    ignore_fb_changed = False
    
    # Database, necessary only for closeEvent handler
    db = None
    
    # main text editor widget; it must be assigned to the field of class
    # or object because it would be removed from memory otherwise
    editor = None

    def __init__(self, db):
        """Prepares everything that Qt needs.
        """
        super().__init__()
        self.register_excepthook()
        self.init_ui(db)
        
    def register_excepthook(self):
        """Any run time error will be shown in a MsgBox instead of printing
           it to the console by default.
        """
        def excepthook(type, value, traceback):
            QMessageBox.warning(self, 'Error', type.__name__ + ': ' + str(value))
        sys.excepthook = excepthook

    def init_ui(self, db):
        """Initializes main window.
        """
        self.db = db
        
        editor = XmlEditor()
        self.setCentralWidget(editor)
        editor.textChanged.connect(partial(fb_changed, self, db))
        self.editor = editor
        
        act_new = QAction(QIcon('icons/new.png'), 'New', self)
        act_new.setShortcut('Ctrl+N')
        act_new.setStatusTip('Create new file')
        act_new.triggered.connect(partial(fb_new, self, db))
        
        act_open = QAction(QIcon('icons/open.png'), 'Open...', self)
        act_open.setShortcut('Ctrl+O')
        act_open.setStatusTip('Open file')
        act_open.triggered.connect(partial(fb_open, self, db))
        
        act_save = QAction(QIcon('icons/save.png'), 'Save', self)
        act_save.setShortcut('Ctrl+S')
        act_save.setStatusTip('Save file')
        act_save.triggered.connect(partial(fb_save, self, db))
        
        act_saveas = QAction(QIcon('icons/saveas.png'), 'Save As...', self)
        act_saveas.setShortcut('Ctrl+Alt+S')
        act_saveas.setStatusTip('Save file as')
        act_saveas.triggered.connect(partial(fb_save_as, self, db, True))
        
        act_exit = QAction(QIcon('icons/exit.png'), 'Exit', self)
        act_exit.setShortcut('Ctrl+Q')
        act_exit.setStatusTip('Exit application')
        act_exit.triggered.connect(partial(fb_exit, self, db))
        
        act_addlicense = QAction(QIcon('icons/add.png'), 'Add License', self)
        act_addlicense.setShortcut('Ctrl+Alt+L')
        act_addlicense.setStatusTip('Add new license')
        act_addlicense.triggered.connect(partial(fb_add_license, self, db))
        
        act_addpackage = QAction(QIcon('icons/add.png'), 'Add Package', self)
        act_addpackage.setShortcut('Ctrl+Alt+P')
        act_addpackage.setStatusTip('Add new package')
        act_addpackage.triggered.connect(partial(fb_add_package, self, db))
        
        act_addversion = QAction(QIcon('icons/add.png'), 'Add Version', self)
        act_addversion.setShortcut('Ctrl+Alt+V')
        act_addversion.setStatusTip('Add new version')
        act_addversion.triggered.connect(partial(fb_add_version, self, db))
        
        act_clone = QAction(QIcon('icons/clone.png'), 'Clone Item', self)
        act_clone.setShortcut('Ctrl+Alt+C')
        act_clone.setStatusTip('Clone item')
        act_clone.triggered.connect(partial(fb_clone_item, self, db))
        
        act_delete = QAction(QIcon('icons/delete.png'), 'Delete Item', self)
        act_delete.setShortcut('Ctrl+Alt+D')
        act_delete.setStatusTip('Delete item')
        act_delete.triggered.connect(partial(fb_delete_item, self, db))

        act_home = QAction(QIcon('icons/www.png'), 'Npackd Home Page', self)
        act_home.setStatusTip('Npackd home page')
        act_home.triggered.connect(partial(webbrowser.open, 'https://npackd.appspot.com'))
        
        act_doc_repo = QAction(QIcon('icons/www.png'), 'Repository Format', self)
        act_doc_repo.setShortcut('F1')
        act_doc_repo.setStatusTip('Online help')
        act_doc_repo.triggered.connect(partial(webbrowser.open, 'https://code.google.com/p/windows-package-manager/wiki/RepositoryFormat'))
        
        act_doc_scripts = QAction(QIcon('icons/www.png'), 'Installation Scripts', self)
        act_doc_scripts.setStatusTip('Online help')
        act_doc_scripts.triggered.connect(partial(webbrowser.open, 'https://code.google.com/p/windows-package-manager/wiki/InstallationScripts'))
        
        act_example = QAction(QIcon('icons/www.png'), 'Sample Repository', self)
        act_example.setStatusTip('Example of repository')
        act_example.triggered.connect(partial(webbrowser.open, 'https://npackd.appspot.com/rep/xml?tag=stable'))

        act_about = QAction(QIcon('icons/about.png'), 'About...', self)
        act_about.setStatusTip('About Repo Editor')
        act_about.triggered.connect(partial(self.show_about, db))
        
        self.statusBar()
        mnu_bar = self.menuBar()
        mnu_file = mnu_bar.addMenu('&File')
        mnu_file.addAction(act_new)
        mnu_file.addAction(act_open)
        mnu_file.addAction(act_save)
        mnu_file.addAction(act_saveas)
        mnu_file.addSeparator()
        mnu_file.addAction(act_exit)

        mnu_edit = mnu_bar.addMenu('&Edit')
        mnu_edit.addAction(act_addlicense)
        mnu_edit.addAction(act_addpackage)
        mnu_edit.addAction(act_addversion)
        mnu_edit.addSeparator()
        mnu_edit.addAction(act_clone)
        mnu_edit.addAction(act_delete)

        mnu_licenses = mnu_bar.addMenu('&Licences')
        mnu_packages = mnu_bar.addMenu('&Packages')
        mnu_versions = mnu_bar.addMenu('&Versions')
        
        mnu_help = mnu_bar.addMenu('&Help')
        mnu_help.addAction(act_home)
        mnu_help.addAction(act_doc_repo)
        mnu_help.addAction(act_doc_scripts)
        mnu_help.addAction(act_example)
        mnu_help.addSeparator()
        mnu_help.addAction(act_about)

        self.dynamic_menus['license'] = (mnu_licenses, fb_select_license)
        self.dynamic_menus['package'] = (mnu_packages, fb_select_package)
        self.dynamic_menus['version'] = (mnu_versions, fb_select_version)
        
        screen = QDesktopWidget().screenGeometry()
        w = 1000
        h = 400
        self.setGeometry((screen.width() - w)//2, (screen.height() - h)//2, w, h)
        self.setWindowIcon(QIcon('icons/repoeditor.png'))
        fb_new(self, db)
        self.show()
        
    def closeEvent(self, event):
        """Feedback called when user tries to close main window. Operation
           can be canceled if the changes are not saved.
        """
        try:
            self.discard_unsaved_changes(self.db)
            event.accept()
        except ExCanceledByUser as ex:
            event.ignore()
                
    def set_menu_items(self, db, tag, names):
        """Some of the menus change their content dynamically in runtime.
           This method updates menu specified by 'tag' with the items
           given in 'names'.
        """
        menu, fb = self.dynamic_menus[tag]
        group = QActionGroup(self, exclusive=True)
        menu.clear()
        for name in names:
            action = QAction(name, self, checkable=True)
            action.setStatusTip('Select item')
            action.triggered.connect(partial(fb, self, db, name))
            a = group.addAction(action)
            menu.addAction(a)
            if db.selection[tag] == name:
                a.toggle()

    def update_menus(self, db):
        """Calls set_menu_items for all the tags accordingly.
        """
        for tag in ['license', 'package']:
            self.set_menu_items(db, tag, db.get_names(tag))

        if db.selection['package']:
            versions = db.get_names('version', db.selection['package'])
        else:
            versions = []

        self.set_menu_items(db, 'version', versions)

    def update_title(self, db):
        """Updates title of the main window.
        """
        self.setWindowTitle(db.format_title())
    
    def update(self, db):
        """Updates whole main window.
        """
        self.update_menus(db)
        self.update_title(db)
        
    def clear_text(self):
        """Clears text in the editor without calling feedback
        """
        self.set_text('')
        
    def set_text(self, text):
        """Sets text in the editor without calling feedback
        """
        self.ignore_fb_changed = True
        self.editor.setText(text)
    
    def load_from_template(self, db, tag):
        """Loads text to the editor from template given by 'tag'.
        """
        path = os.path.join('templates', tag + '.xml')
        with open(path, 'r') as f:
            text = f.read()

        vars_ = db.get_vars()
        self.editor.setText(text.format(**vars_))

    def show_message(self, msg):
        """Shows 'msg' message in status bar of the main window.
        """
        bar = self.statusBar()
        bar.showMessage(msg)

    def discard_unsaved_changes(self, db):
        """Shows prompt if there are unsaved changes. Current
           operation will be discarded if the user decides so.
        """
        if db.changed and not db.empty:
            answer = QMessageBox.question(self, 'Continue?', 'Unsaved changes will be lost, would you like to continue?', QMessageBox.Ok, QMessageBox.Cancel)
            if answer == QMessageBox.Cancel:
                raise ExCanceledByUser()
                
    def show_about(self, db):
        """Shows MsgBox with information about the application.
        """
        msg = 'npackd-repoeditor ' + APP_VERSION + """
Author: Grzegorz Krasoń

This application is intended to be used for editing small and medium size repositories of Npackd package manager.
        """
        QMessageBox.question(self, 'User Manual', msg, QMessageBox.Ok)

    def ask_file_path(self, open=False):
        """Shows Open/Save file dialog.
        """
        if open:
            file_path = QFileDialog.getOpenFileName(self, 'Open repo', '', '*.xml')
        else:
            file_path = QFileDialog.getSaveFileName(self, 'Save repo', 'untitled', '*.xml')

        if not file_path:
            raise ExCanceledByUser()

        return file_path
        
    def confirm_deletion(self, name):
        """Shows MsgBox that asks the user for confirmation if he would
           like to delete an item of the name 'name'.
        """
        answer = QMessageBox.question(self, 'Delete?', 'Are you sure you would like to delete ' + name + '?', QMessageBox.Ok, QMessageBox.Cancel)
        if answer == QMessageBox.Cancel:
            raise ExCanceledByUser()

    def apply_changes(self, db):
        """Tries to transfer changes from the editor to the database.
        """
        nothing_tbd = False
        
        xml = self.editor.toPlainText()
        if not db.changed:
            nothing_tbd = True

        try:
            # parse items in the editor
            root_tmp = ET.fromstring('<root>' + xml + '</root>')
        except ET.ParseError as e:
            raise ExCanceledByError('Syntax error!')

        items_tmp = [item for item in root_tmp.iterfind('*') if item.tag in ['license', 'package', 'version']]

        if len(items_tmp) > 1:
            raise ExCanceledByError('Please edit at most one item at a time!')

        if len(items_tmp) == 0 and db.last_tag == None:
            nothing_tbd = True

        if not nothing_tbd:
            if len(items_tmp) == 0:
                # remove currently selected item
                item = None
            else:
                # create/update/rename item
                item = items_tmp[0]
                if not item.attrib['name']:
                    raise ExCanceledByError('Please specify the name')
                    
                if item.tag == 'version' and item.attrib['package'] not in db.get_names('package'):
                    raise ExCanceledByError('Please specify valid package')

            db.overwrite_item(item)
            db.sort()
            db.select(item)
            self.update(db)
