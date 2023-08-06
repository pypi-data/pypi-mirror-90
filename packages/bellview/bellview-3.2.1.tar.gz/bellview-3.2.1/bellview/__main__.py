######################################################################
### Bell View
### Copyright (c) 2021 Jonathan Wilson
### Please refer to help/licence.txt for further information
### File: __main__.py
### Description: Bell View GUI
### Last Modified: 3 January 2021
######################################################################

from sys import argv, exit
from .bvapp import BellViewApp

r=BellViewApp().run_app(argv[1:])
exit(r)




