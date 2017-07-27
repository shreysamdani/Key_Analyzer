import pandas as pd 
import xlsxwriter
import os
from colorama import init, Fore, Back, Style

############# TEMPLATE CODE ##########################
############# RUN THIS FILE IN TERMINAL ##########################


xl = pd.read_excel(os.path.basename(__file__)[:-len('Functions.py')] + 'Analysis.xlsx', 'Basic Calculations', encoding='utf-8')
column = [i for i in xl]

hex_seeds = list(xl[column[0]].dropna()[:])
hex_keys = list(xl[column[1]].dropna()[:])

dec_seeds = list(xl[column[2]].dropna()[:])
dec_keys = list(xl[column[3]].dropna()[:])

bin_seeds = list(xl[column[4]].dropna()[:])
bin_keys = list(xl[column[5]].dropna()[:])

<<<<<<< HEAD
=======
# add leading zeros to binary representations
bits = len(hex_seeds[0]) * 4
bin_seeds = [(bits - len(i)) * "0" + str(i) for i in bin_seeds]
bin_keys = [(bits - len(i)) * "0" + str(i) for i in bin_keys]

>>>>>>> fa0c0ab6a95fb47243be0a64c0f6da8801019656
# Fill in this function accordingly to solve the problem
def function(x):
	# Your Code Here
	return x


# Calculates the error (arithmetic difference) between the
# function's output and the expected output
def getError(g):
	if int(dec_keys[i]) - int(g) != 0:
		return " " + str(int(dec_keys[i]) - int(g)) + " "
	return ""

# Prints to terminal

init()
fontcolor = "red"
bgcolor = "reset"

def cprint(foreground = fontcolor, background = bgcolor):
    fground = foreground.upper()
    bground = background.upper()
    style = getattr(Fore, fground) + getattr(Back, bground)
    return (style, Style.RESET_ALL)

pr = cprint()
print("SEED" + "\t", "PRED" + "\t", 
			"ACTUAL" + "\t", pr[0] + "ERROR" + pr[1])    

k = (str(i) for i in map(function, dec_seeds))
for i in range(len(dec_seeds)):
	g = next(k)
	print(str(dec_seeds[i]) + "\t", str(g) + "\t", 
		str(dec_keys[i]) + "\t", pr[0] + getError(g) + pr[1])
