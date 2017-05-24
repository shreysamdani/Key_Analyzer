import pandas as pd 
import xlsxwriter
import os
from colorama import init, Fore, Back, Style

############# TEMPLATE CODE ##########################
############# RUN THIS FILE IN TERMINAL ##########################


xl = pd.read_excel(os.path.basename(__file__)[:-len('Functions.py')] + 'Analysis.xlsx', 'Basic Calculations', encoding='utf-8')
column = list(xl)

hex_seeds = list(xl[column[0]][:])
hex_keys = list(xl[column[1]][:])

dec_seeds = list(xl[column[2]][:])
dec_keys = list(xl[column[3]][:])

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

def cprint(foreground = "red", background = "black"):
    fground = foreground.upper()
    bground = background.upper()
    style = getattr(Fore, fground) + getattr(Back, bground)
    return (style, Style.RESET_ALL)

k = (str(i) for i in map(function, dec_seeds))
for i in range(len(dec_seeds)):
	g = next(k)
	pr = cprint()
	print(str(dec_seeds[i]) + "\t", str(g) + "\t", 
		str(dec_keys[i]) + "\t", pr[0] + getError(g) + pr[1])