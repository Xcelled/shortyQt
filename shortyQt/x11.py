from .shorty import _ShortyBase

from Xlib import X, XK, threaded
from Xlib.display import Display
from Xlib.ext import xinput
from Xlib.protocol.request import GrabKey, UngrabKey
from Xlib.keysymdef import latin1

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence

from threading import Thread
from weakref import WeakValueDictionary

class XKeyListener(Thread):
	def __init__(self, display, root):
		super().__init__()
		self.daemon = True
		self.display = display
		self.root = root
		self.listenFor = WeakValueDictionary()
		self.start()
	#enddef

	def run(self):
		self.root.xinput_select_events([(xinput.AllDevices, xinput.KeyPressMask)])
		while True:
			event = self.display.next_event()
			if event.type == X.KeyPress:
				cb = self.listenFor.get((event.detail, event. state), None)
				if cb: cb.trigger()
			#endif
		#endwhile
	#enddef

	def register(self, key, mods, sk):
		self.listenFor[(key, mods)] = sk
	#enddef

	def unregister(self, key, mods):
		del self.listenFor[(key, mods)]
	#enddef
#endclass

class X11Shorty(_ShortyBase):
	display = Display()
	root = display.screen().root
	listener = XKeyListener(display, root)

	def __init__(self, shortcut, *args, **kwargs):
		_ShortyBase.__init__(self, shortcut)

		# TODO: Should these change?
		self.display = X11Shorty.display
		self.root = X11Shorty.root
		self.listener = X11Shorty.listener

		self.ignored = [0, X.LockMask, X.Mod2Mask, X.LockMask | X.Mod2Mask]
		self.nativeKey = self.display.keysym_to_keycode(self.nativeKey)
	#enddef

	def __del__(self):
		self.display.close()
		super().__del__()
	#enddef

	def trigger(self, *args, **kwargs): self.activated.emit(*args, **kwargs)

	def _grabKey(self, keycode, modifiers, window):
		GrabKey(self.display.display, owner_events=True, grab_window=window,
				modifiers=modifiers, key=keycode,
				pointer_mode=X.GrabModeAsync, keyboard_mode=X.GrabModeAsync)

		self.listener.register(keycode, modifiers, self)
		
		return True # TODO: error handling?
	#enddef

	def _ungrabKey(self, keycode, modifiers, window):
		UngrabKey(self.display.display, grab_window=window,	modifiers=modifiers, key=keycode)
		self.listener.unregister(keycode, modifiers)

		return True # TODO: error handling?
	#enddef

	def toNativeKeycode(self, key):
		''' Returns the X11 native keycode for a QT Key '''

		keysim = XK.string_to_keysym(QKeySequence(key).toString())
		if keysim == X.NoSymbol:
			keysim = int(key)
		#endif

		return keysim
	#enddef

	def toNativeModifiers(self, flags):
		''' Converts the standard modifier flags to X's '''
		map = zip(
			[Qt.ShiftModifier, Qt.ControlModifier, Qt.AltModifier, Qt.MetaModifier],
			[X.ShiftMask     , X.ControlMask     , X.Mod1Mask    , X.Mod4Mask     ]
			)

		native = 0
		for mod, n in map:
			if flags & mod: native |= n
		#endfor

		return native
	#enddef

	def registerShortcut(self):
		# X has a stupid system where even the numlock counts as
		# a modifier. So have to register multiple hotkeys, one for
		# each combination of modifiers we don't care about
		
		for i in self.ignored:
			if not self._grabKey(self.nativeKey, self.nativeMods | i, self.root): return False
		#endfor

		return True
	#enddef

	def unregisterShortcut(self):
		for i in self.ignored:
			self._ungrabKey(self.nativeKey, self.nativeMods | i, self.root)
		#endfor
	#enddef
#enddef