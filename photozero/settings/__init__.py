from .production import *

try:
	from .local import *
	live = False
except:
	live = True