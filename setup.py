# from distutils.core import setup
# import py2exe
#
# setup(console=['main.py'])
from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')

excludes = ["pywin", "pywin.debugger", "pywin.debugger.dbgcon",
            "pywin.dialogs", "pywin.dialogs.list", "win32com.server",
            "email"]
setup(
    options = {'py2exe': {'bundle_files': 3, 'compressed': True, "excludes": excludes}},
    windows = [{'script': "main.py"}],
    zipfile = None,
)