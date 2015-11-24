import xml.etree.ElementTree as ET
from PyQt4.QtGui import QFileDialog, QMessageBox

# Operation has to be canceled. Something went wrong.
class ExCanceledByError(Exception): pass

# Operation has to be canceled. User changed his mind.
class ExCanceledByUser(Exception): pass

def cancellable(func):
    """Decorator that wraps given feedback function and catches ExCancel*
       exceptions which may occure. This results in cancelling operation
       performed by the feedback function.
    """
    def wrapper(win, db, *args, **kwargs):
        try:
            # that's a hack which allows QT to pass extra arguments to the callback
            args_ = args[:func.__code__.co_argcount-2]
            func(win, db, *args_, **kwargs)
        except ExCanceledByError as ex:
            QMessageBox.warning(win, 'Error', str(ex))
        except ExCanceledByUser as ex:
            win.update(db)

    return wrapper

def add_item(win, db, tag, clone=False):
    """Helper function for fb_add_* functions
    """
    win.discard_unsaved_changes(db)
    db.last_tag = None
    db.selection[tag] = None
    if not clone:
        win.load_from_template(db, tag)
    root = db.tree.getroot()
    if tag == 'package':
        win.set_menu_items(db, 'version', [])
    win.update(db)

def select_item(win, db, tag, name):
    """Helper function for fb_select_* functions
    """
    win.discard_unsaved_changes(win.db)
    db.changed = False
    db.last_tag = tag
    db.selection[tag] = name
    xml = db.get_xml(tag, name)
    win.set_text(xml)
    win.show_message('Selected {}: {}'.format(tag, name))

def fb_new(win, db):
    """Creates new file. Also called at applicatino startup.
    """
    db.reset()
    win.clear_text()
    win.update(db)

@cancellable
def fb_open(win, db):
    """Opens file
    """
    win.discard_unsaved_changes(db)
    file_path = win.ask_file_path(open=True)
    db.load(file_path)
    win.clear_text()
    win.update(db)

def fb_save(win, db):
    """Saves file if path is known, otherwise prompts for the path first
    """
    fb_save_as(win, db, ask=(db.file_path==None))

@cancellable
def fb_save_as(win, db, ask):
    """Prompts for the paht and saves the file
    """
    win.apply_changes(db)
    if ask:
        file_path = win.ask_file_path(open=False)
        db.save(file_path)
    else:
        db.save()
    win.update_title(db)
        
def fb_exit(win, db):
    """Closes application, but first makes sure that changes have been saved
    """
    win.close()

@cancellable
def fb_add_license(win, db):
    """Adds new license
    """
    add_item(win, db, 'license')

@cancellable
def fb_add_package(win, db):
    """Adds new package, field 'license' equals to recently selected license
    """
    add_item(win, db, 'package')

@cancellable
def fb_add_version(win, db):
    """Adds new package, field 'package name' equals to recently selected package
    """
    add_item(win, db, 'version')
    
@cancellable
def fb_clone_item(win, db):
    """Clears selection and updates status flags
    """
    if db.last_tag:
        add_item(win, db, db.last_tag, clone=True)
        db.changed = True
        win.update_title(db)
    else:
        win.show_message('Nothing to clone')

def fb_delete_item(win, db):
    """Clears text editor and updates status flags
    """
    if db.last_tag:
        win.clear_text()
        db.changed = True
        win.update_title(db)
    else:
        win.show_message('Nothing to delete')
        
@cancellable
def fb_select_license(win, db, name):
    """Selects license
    """
    select_item(win, db, 'license', name)

@cancellable
def fb_select_package(win, db, name):
    """Selects package
    """
    select_item(win, db, 'package', name)
    db.selection['version'] = None
    root = db.tree.getroot()
    versions = db.get_names('version', name)
    win.set_menu_items(db, 'version', versions)

@cancellable
def fb_select_version(win, db, name):
    """Selects version
    """
    select_item(win, db, 'version', name)

def fb_changed(win, db):
    """Updates flags when text in text editor is changed
    """
    if not win.ignore_fb_changed:
        db.mark_changed()
        win.update_title(db)
    win.ignore_fb_changed = False
