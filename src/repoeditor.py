#!/usr/bin/env python3

import sys
from PyQt4.QtGui import QApplication
from lib.database import Database
from lib.gui import Gui
            
def main():
    """Starts Qt GUI and connects it to database.
       This function never returns to its caller.
    """
    app = QApplication(sys.argv)
    db = Database()
    gui = Gui(db)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
