# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# Allow us to find shortyQt from the examples folder
import sys, os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QKeySequence

from shortyQt import Shorty

SHORTCUT_SHOW = QKeySequence("Ctrl+shift+k")  # Ctrl maps to Command on Mac OS X
SHORTCUT_EXIT = QKeySequence("Ctrl+shift+j")  # again, Ctrl maps to Command on Mac OS X

def showActivated():
	print("Shorty called!")
#enddef

app = QApplication([])

show = Shorty(SHORTCUT_SHOW)
show.activated.connect(showActivated)
show.enable()

quit = Shorty(SHORTCUT_EXIT)
quit.activated.connect(app.exit)
quit.enable()

app.exec_()

show.disable() # Not needed, as deleteing a shortcut disables it
quit.disable() # Not needed, as deleteing a shortcut disables it

del show
del quit