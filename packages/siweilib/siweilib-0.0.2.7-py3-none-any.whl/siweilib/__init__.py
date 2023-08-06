import os

f = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'VERSION.txt'))
s = f.read()
f.close()

__version__ = s

import siweilib.general
import siweilib.general as g