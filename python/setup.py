from cx_Freeze import setup, Executable

setup( name = "" , version = "0.1" , description = "test" , executables = [Executable("all.py")] , options = {
        "build_exe" : {
        	"packages": ['pandas', 'xlsxwriter', 'numpy'],
            "excludes": ['tcl', 'ttk', 'tkinter', 'Tkinter'],
            "optimize": 2 
        }})