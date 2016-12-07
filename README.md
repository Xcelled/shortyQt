# shortyQt
Cross Platform global shortcut (hotkey) library written using Python and QT5.

Currently only X11 is supported, but Windows is coming soon.

#Minimal example:
```
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QKeySequence

from shortyQt import Shorty

SHORTCUT_EXIT = QKeySequence("Ctrl+shift+j")  # Ctrl maps to Command on Mac OS X
app = QApplication([])

quit = Shorty(SHORTCUT_EXIT)
quit.activated.connect(app.exit)
quit.enable()

app.exec_()
```

# OS-based deps
 On linux, you need to install `python-xlib` from pip.

# Usage
## Backends
The correct backend is selected automatically and provided as `shortyQt.Shorty`.

If you want to use another backend, you can use these:

- `shortyQt.x11.X11Shorty` - X11 Backend using python-xlib

## Creating a shortcut
Simply pass a QKeySequence to the Shorty constructor.

## Enable/Disable
Shortcuts must be enabled before they'll work. Just call the enable method. You can disable a shortcut with `disable()`.

## Getting notified
Hook up to the `activated` signal on a Shorty instance to be notified when the shortcut is run