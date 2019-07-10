from cx_Freeze import setup, Executable

import os.path
import sys

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

include_files = [os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
                 os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'), ]

options = {'build_exe': {
    "includes": ["numpy", "tkinter", "pandas", "PIL", "cv2", "scipy", "matplotlib"],
    "include_files": include_files,
    "excludes": [],
    "optimize": 2}
}
setup(
    name="BlackJack",
    version="1.0.0",
    description="Singleplayer BlackJack with GUI",
    executables=[Executable("BlackJack.py", targetName='BlackJack.exe')],
    options=options
)
