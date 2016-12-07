from PyQt5.QtCore import QObject, pyqtSignal, Qt

class _ShortyBase(QObject):
	''' Base class for all shortcuts '''
	activated = pyqtSignal()

	def __init__(self, shortcut, *args, **kwargs):
		QObject.__init__(self)
		self.shortcut = shortcut
		self.enabled = False

		# extract key and mods
		allMods = int(Qt.ShiftModifier | Qt.ControlModifier | Qt.AltModifier | Qt.MetaModifier)
		key = 0 if shortcut.isEmpty() else shortcut[0] & ~allMods
		mods = 0 if shortcut.isEmpty() else shortcut[0] & allMods

		self.nativeKey = self.toNativeKeycode(key)
		self.nativeMods = self.toNativeModifiers(mods)
	#enddef

	def __del__(self):
		self.disable()
		try: super().__del__(self)
		except: pass
	#enddef

	def isEnabled(self):
		return self.enabled
	#enddef

	def enable(self):
		if self.enabled: return
		self.registerShortcut()
		self.enabled = True
	#enddef

	def disable(self):
		if not self.enabled: return
		self.unregisterShortcut()
		self.enabled = False
	#enddef
#endclass