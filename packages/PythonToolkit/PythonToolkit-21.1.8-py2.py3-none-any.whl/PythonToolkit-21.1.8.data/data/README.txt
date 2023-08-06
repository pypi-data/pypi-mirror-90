README.txt
----------
Python Toolkit (ptk) is an interactive environment for python. Based around a 
set of interacting tools it includes an interactive console (with support for 
multiple python interpreters and GUI mainloops), a simple python source editor,
a python path manager and namespace browser.

For help tips, feature requests, bug reports, ideas or to contact me please use
the sourceforge project pages:

http://sourceforge.net/projects/pythontoolkit/
http://pythontoolkit.sourceforge.net
tohc1@users.sourceforge.net

T.Charrett, 2011

INSTALLING
----------
PTK can be started simply by extracting the source and running PTK.pyw. 
(ensure PTK.pyw and PTKengine.pyw are executable)

Alternatively PTK can now installed as a package (ptk_lib) using python 
distutils. This allows python engines to be embedded in other python 
applications allowing the PTK interface to control exectution/insepction in the
host application.

To install extract the source, and run:

$ python setup.py install

This will install the ptk package in the usual python location for your system 
along with a PTK lauch script.

MAC
---
It should be possible to run PTK on a Mac (via wxPython) although at least 
python 2.6 is required and it is untested. I would be grateful to hear of any
issues or suggestion for running on Mac os. Please contact me via the above 
email address.

UPGRADING
---------
If you are upgrading from previous versions the configuration may have changed
between versions, this can give strange effects with window layouts etc. To fix
any problems it is recommended to run:

PTK --clear_settings

This will clear any previously stored settings from previous versions. 
Alternatively you can delete the .PTK folder in the home directory.

LICENSE
-------
MIT compatible see LICENSE.txt
