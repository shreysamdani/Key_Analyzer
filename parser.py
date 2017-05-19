import pandas as pd
import xlsxwriter
import sys
import os
import calcs
import rotatesShifts
import platform

# read in the file
xl = pd.read_excel(str(sys.argv[1]), 'Seed_Keys_Samples', encoding='utf-8')
seeds = xl['2 bytes'][1:]
keys = xl['Unnamed: 1'][1:]

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


# create a new excel file 
file = str(sys.argv[1])[:-5] + ' Analysis.xls'
workbook = xlsxwriter.Workbook(file)

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

############################### CALCULATIONS ########################################
binaries = calcs.binDiff(binKeys, rFont, font)
differences = calcs.differences(decSeeds, decKeys)
secondDifferences = calcs.sDifferences(differences)
xorBin, xorDec = calcs.xor(binKeys)
diffs, diffInstances = calcs.mostCommon(differences)
xors, xorInstances = calcs.mostCommon(xorDec)

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
row += 1

# write in the columns for calculations
for i in range(len(seeds)):
    calculations.write(row, 0, hexSeeds[i], font)
    calculations.write(row, 1, hexKeys[i], font)
    calculations.write(row, 2, decSeeds[i], font)
    calculations.write(row, 3, decKeys[i], font)
    calculations.write(row, 4, binSeeds[i], font)
    calculations.write_rich_string(row, 5, *binaries[i])

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

######################### SHIFTS AND ROTATES ##########################################
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
row += 1

for i in range(length - 1):
    shifts.write(row, i, 'RIGHT ' + str(i + 1), bFont)
for i in range(length - 1):
    shifts.write(row, i + length, 'LEFT ' + str(i + 1), bFont)
for i in range(length - 1):
    shifts.write(row, i + 2 * length, 'ROTATE ' + str(i + 1), bFont)
for i in range(length - 1):
    shifts.write(row, i + 3 * length, 'MASK ' + str(i + 1), bFont)
row += 1

for i in range(length - 1):
    for j in range(len(binKeys)):
        shifts.write(row, i, rshifts[i][j] , font)
        shifts.write(row, i + length, lshifts[i][j], font)
        shifts.write(row, i + 2 * length, rotates[i][j], font)
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
# close the workbook and open the file
workbook.close()

if platform.system() == 'Windows':
    os.startfile(file.replace(" ", "\ "))
else:
    os.system("open " + file.replace(" ", "\ "))
