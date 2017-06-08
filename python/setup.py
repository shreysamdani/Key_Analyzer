from cx_Freeze import setup, Executable
import sys

base = None
if sys.platform == 'win32':
	base = 'Win32GUI'

setup( name = "" , version = "0.1" , description = "Creates the Analyzer workbook and the template Python file" , executables = [Executable("Analyzer.py", base = "Win32GUI")] , options = {
        "build_exe" : {
        	"packages": ['pandas', 'xlsxwriter', 'numpy'],
            "excludes": ['tcl', 'ttk', 'tkinter', 'Tkinter'],
            "optimize": 2 
        }})