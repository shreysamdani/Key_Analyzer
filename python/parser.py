import pandas as pd
import xlsxwriter
import sys
import os
import calcs
import rotatesShifts
import platform
import shutil 
import subprocess

################################ READ FORMATTED INPUT FILE ##########################
print("Drag and drop your file here: \t")
filename = str(input())
if os.name == 'nt':
    filename = os.path.abspath(filename[3:]).replace("'", "")
xl = pd.read_excel(filename, 'Seed_Keys_Samples', encoding='utf-8')
name_in = filename

############################### CONVERT INPUT INTO COLUMNS ##########################

column = list(xl)
keys = xl[column[1]][1:]
keys.dropna()
seeds = xl[column[0]][1:]
seeds.dropna()

# convert data to specific type
hexSeeds = [str(i) for i in seeds]
hexKeys = [str(i) for i in keys]

decSeeds = [int(str(i), 16) for i in seeds]
decKeys = [int(str(i), 16) for i in keys]

binSeeds = [str(bin(i))[2:] for i in decSeeds]
binKeys = [str(bin(i))[2:] for i in decKeys]

# make sure the binary strings are the correct length
for i in range(len(binSeeds)):
    binSeeds[i] = '0' * (4 * len(hexKeys[1]) - len(binSeeds[i])) + binSeeds[i]
    binKeys[i] = '0' * (4 * len(hexKeys[1]) - len(binKeys[i])) + binKeys[i]

################################ BUILDING NEW EXCEL FILE ##########################

# create a new excel file
file = name_in[:name_in.find(".xls")]
workbookName = file + ' Analysis.xlsx'
workbook = xlsxwriter.Workbook(workbookName)

################################ BUILDING NEW PYTHON FILE ##########################

pythonFileName = file + ' Functions.py'
shutil.copyfile('template.py', pythonFileName)

################################ CREATE FOLDER STRUCTURE ########################## 

# decide where to keep new directory
# print('This program saves program files in a directory. Please paste your current directory. Type \"def\" for a default directory on your desktop.\n')
# location = str(input())

# # go to user's home path
# userhome = os.path.expanduser('~')
# useros = platform.system()
# if location == 'def':
#     if useros == 'Windows':
#         location = userhome + '\\Desktop\\'
#     else:
#         location = userhome + '/Desktop/'

# build a folder structure: location --> Data Analyzer --> file folder --> files
# folderPath = os.path.join(location, 'Data Analyzer')
# if not os.path.exists(folderPath):
#     os.makedirs(folderPath)
# subprocess.Popen('explorer \"' + folderPath + '\"')
# subfolderPath = os.path.join(folderPath, file)
# os.makedirs(subfolderPath)
# if os.path.exists(subfolderPath):
#     subprocess.Popen('explorer \"' + subfolderPath + '\"')
#     subprocess.Popen('cd \"' + subfolderPath + '\"', shell = True)

# # put files in their appropriate places

# shutil.copy2(pythonFileName, subfolderPath)
# try:
#     workbookLocation = os.path.abspath(workbookName)
#     shutil.move(workbookLocation, subfolderPath)
# except shutil.Error:
#     print()
# except FileNotFoundError:
#     print()

################################ SETTING UP WORKBOOK ##########################


calculations = workbook.add_worksheet('Basic Calculations')
calculations.set_column(0, 5, 20)
calculations.set_column(7, 8, 20)
calculations.set_column(10, 10, 20)

shifts = workbook.add_worksheet('Rotates and Shifts')
graphs = workbook.add_worksheet('Graphs')

font = workbook.add_format()
font.set_font_name('Courier New')

rFont = workbook.add_format()
rFont.set_font_color('red')
rFont.set_font_name('Courier New')

bFont = workbook.add_format({'bold' : True})
bFont.set_font_name('Courier New')

################### CALCULATIONS WORKSHEET ####################

binaries = calcs.binDiff(binKeys, rFont, font)
differences = calcs.differences(decSeeds, decKeys)
secondDifferences = calcs.sDifferences(differences)
xorBin, xorDec = calcs.xor(binKeys)
diffs, diffInstances = calcs.mostCommon(differences)
xors, xorInstances = calcs.mostCommon(xorDec)
nots = calcs.bitNot(binKeys, rFont, font)

# write in the column titles for calculations
row = 0
calculations.write(row, 0, 'HEX_SEEDS', font)
calculations.write(row, 1, 'HEX_KEYS', font)
calculations.write(row, 2, 'DEC_SEEDS', font)
calculations.write(row, 3, 'DEC_KEYS', font)
calculations.write(row, 4, 'BIN_SEEDS', font)
calculations.write(row, 5, 'BIN_KEYS', font)
calculations.write(row, 7, '1st_DIFFERENCES', font)
calculations.write(row, 8, '2nd_DIFFERENCES', font)
calculations.write(row, 10, 'XOR_BIN', font)
calculations.write(row, 11, 'XOR_DEC', font)
calculations.write(row, 13, 'APPEARANCES (DIFFERENCES)', font)
calculations.write(row, 16, 'APPEARANCES (XOR)', font)
calculations.write(row, 18, 'BIT_NOT', font)
calculations.freeze_panes(1, 0)
row += 1

# write in the columns for calculations
for i in range(len(seeds)):
    calculations.write(row, 0, hexSeeds[i], font)
    calculations.write(row, 1, hexKeys[i], font)
    calculations.write(row, 2, decSeeds[i], font)
    calculations.write(row, 3, decKeys[i], font)
    calculations.write(row, 4, binSeeds[i], font)
    calculations.write_rich_string(row, 5, *binaries[i])
    calculations.write_rich_string(row, 18, *nots[i])

    if i < len(seeds) - 1:
        calculations.write(row, 7, differences[i], font)
        calculations.write(row, 10, xorBin[i], font)
        calculations.write(row, 11, xorDec[i], font)

    if i < len(seeds) - 2:
        calculations.write(row, 8, secondDifferences[i], font)

    row += 1

row = 1
for i in range(len(diffs)):
    calculations.write(row, 13, diffs[i], font)
    calculations.write(row, 14, diffInstances[i], font)
    row += 1

row = 1
for i in range(len(xors)):
    calculations.write(row, 16, xors[i], font)
    calculations.write(row, 17, xorInstances[i], font)
    row += 1

######################### SHIFTS, ROTATES, MASKS ############################

rshifts = rotatesShifts.RshiftAll(binKeys)
lshifts = rotatesShifts.LshiftAll(binKeys)
rotates = rotatesShifts.rotateAll(binKeys)
masks = rotatesShifts.createMasks(binKeys)

length = len(binKeys[0])

shifts.set_column(0, length, 9)
shifts.set_column(length, length * 2, 11)
shifts.set_column(length * 2, length * 3 - 1, 11)
row = 0

shifts.write(row, 0, 'RIGHT_SHIFTS', bFont)
shifts.write(row, length, 'LEFT_SHIFTS', bFont)
shifts.write(row, 2 * length, 'ROTATES', bFont)
shifts.write(row, 3 * length, 'MASKS', bFont)
shifts.freeze_panes(1, 0)
row += 1

for i in range(length - 1):
    shifts.write(row, i, 'RIGHT ' + str(i + 1), bFont)
for i in range(length - 1):
    shifts.write(row, i + length, 'LEFT ' + str(i + 1), bFont)
for i in range(length - 1):
    shifts.write(row, i + 2 * length, 'ROTATE ' + str(i + 1), bFont)
for i in range(length//4):
    shifts.write(row, i + 3 * length, 'MASK 2^' + str(i), bFont)
row += 1
temp = row

for i in range(length - 1):
    for j in range(len(binKeys)):
        shifts.write(row, i, rshifts[i][j] , font)
        shifts.write(row, i + length, lshifts[i][j], font)
        shifts.write(row, i + 2 * length, rotates[i][j], font)
        row += 1
    row = 2

row = temp
for i in range(length//4):
    for j in range(len(binKeys)):
        shifts.write(row, i + 3 * length, masks[i][j], font)
        row += 1
    row = 2

################################### GRAPHS ##########################################

seedGraph = workbook.add_chart({'type' : 'line', 'subtype' : 'straight_with_markers'})
seedGraph.set_title({'name' : 'Key vs Seed'})

diffGraph = workbook.add_chart({'type' : 'scatter', 'subtype' : 'straight_with_markers'})
diffGraph.set_title({'name' : '1st Differences vs Seed'})

sdiffGraph = workbook.add_chart({'type' : 'scatter', 'subtype' : 'straight_with_markers'})
sdiffGraph.set_title({'name' : '2nd Differences vs Seed'})

xorGraph = workbook.add_chart({'type' : 'scatter', 'subtype' : 'straight_with_markers'})
xorGraph.set_title({'name' : 'XOR vs Seed'})


seedGraph.add_series({'values' : '=Basic Calculations!$D$2:$D$' + str(len(binKeys) + 1),
                      'categories': '=Basic Calculations!$C$2:$C$' + str(len(binKeys) + 1)})

diffGraph.add_series({'values' : '=Basic Calculations!$H$2:$H$' + str(len(binKeys) + 1),
                      'categories': '=Basic Calculations!$C$2:$C$' + str(len(binKeys))})

sdiffGraph.add_series({'values' : '=Basic Calculations!$I$2:$I$' + str(len(binKeys) + 1),
                       'categories': '=Basic Calculations!$C$2:$C$' + str(len(binKeys) - 1)})

xorGraph.add_series({'values' : '=Basic Calculations!$L$2:$L$' + str(len(binKeys) + 1),
                     'categories': '=Basic Calculations!$C$2:$C$' + str(len(binKeys))})

graphs.insert_chart(1, 1, seedGraph)
graphs.insert_chart(1, 9, diffGraph)
graphs.insert_chart(17, 1, sdiffGraph)
graphs.insert_chart(17, 9, xorGraph)


def find_consecutive_range():
    f = 0
    while decSeeds[f] + 1 != decSeeds[f + 1]:
        f += 1
    l = f
    while decSeeds[l] + 1 == decSeeds[l + 1]:
        l += 1
    return f, l

def find_bitwalk():
    f = 0
    while decSeeds[f] * 2 != decSeeds[f + 1]:
        f += 1
    l = f 
    while decSeeds[l] * 2 == decSeeds[l + 1]:
        l += 1
    return f, l

consecutiveGraph = workbook.add_chart({'type' : 'scatter', 'subtype' : 'straight_with_markers'})
consecutiveGraph.set_title({'name' : 'Key vs Seed (Consecutive Seeds)'})
first, last = find_consecutive_range()
if last - first > 0:
    consecutiveGraph.add_series({'values' : '=Basic Calculations!$D$' + str(first) + ':$D$' + str(last),
                      'categories': '=Basic Calculations!$C$' + str(first) + ':$C$' + str(last)})
graphs.insert_chart(33, 1, consecutiveGraph)

bitwalkGraph = workbook.add_chart({'type' : 'scatter', 'subtype' : 'straight_with_markers'})
bitwalkGraph.set_title({'name' : 'Key vs Seed (Power-2 Seeds)'})
first, last = find_bitwalk()
if last - first > 0:
    bitwalkGraph.add_series({'values' : '=Basic Calculations!$D$' + str(first) + ':$D$' + str(last),
                      'categories': '=Basic Calculations!$C$' + str(first) + ':$C$' + str(last)})
graphs.insert_chart(33, 9, bitwalkGraph)

try:
    # close the workbook
    workbook.close()

################################ OPEN FILES ##########################  
    if platform.system() == 'Windows':
        os.startfile(os.path.abspath(pythonFileName))
        os.startfile(os.path.abspath(workbookName))
    else:
        os.system("open " + pythonFileName.replace(" ", "\\ "))
        os.system("open " + workbookName.replace(" ", "\\ "))
except PermissionError:
    print()