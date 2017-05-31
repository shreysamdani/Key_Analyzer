# Tool created by Aditya Varshney and Shrey Samdani


import pandas as pd
import xlsxwriter
import sys
import os
import calcs
import rotatesShifts
import platform
import shutil 
import subprocess

    #################### ALL FUNCTIONS ############################################

def run(file):


    filename = file.replace("\ ", " ").strip()

    def rotateAll(binKeys):
        all = []
        for i in range(1, len(binKeys[0])):
            all.append(performLRotation(binKeys, i))
        return all

    def LshiftAll(binKeys):
        all = []
        for i in range(1, len(binKeys[0])):
            all.append(performLShift(binKeys, i))
        return all

    def RshiftAll(binKeys):
        all = []
        for i in range(1, len(binKeys[0])):
            all.append(performRShift(binKeys, i))
        return all

    def performLRotation(binKeys, k):
        leftRotatedKeys = []
        for i in binKeys:
            leftRotatedKeys.append(int(i[k:] + i[:k], 2))
        return leftRotatedKeys

    def performRRotation(binKeys, k):
        rightRotatedKeys = []
        for binaryKey in binKeys:
            rightRotatedKeys.append(binaryKey[(-1 * k):] + binaryKey[:(-1 * k)])
        return rightRotatedKeys

    def performLShift(binKeys, k):
        leftShiftedKeys = []
        for binaryKey in binKeys:
            leftShiftedKeys.append(int(binaryKey, 2) << k)
        return leftShiftedKeys

    def performRShift(binKeys, k):
        rightShiftedKeys = []
        for binaryKey in binKeys:
            rightShiftedKeys.append(int(binaryKey, 2) >> k)
        return rightShiftedKeys

    def createMasks(binKeys):
        return [[int(binaryKey, 2) & int(str(2 ** i), 16) for binaryKey in binKeys] for i in range(0, len(binKeys[0])//2)]

    # create the differences column
    def differences(decSeeds, decKeys):
        diffs = []
        for i in range(len(decSeeds) - 1):
            diffs.append(decKeys[i + 1] - decKeys[i])
        return diffs


    # create the second differences from the first differences column
    def sDifferences(differences):
        secondDifferences = []
        for i in range(len(differences) - 1):
            secondDifferences.append(differences[i + 1] - differences[i])
        return secondDifferences


    # create the xor column
    def xor(binKeys):
        xorBin = []
        for i in range(len(binKeys) - 1):
            xorBin.append(''.join(str(ord(a) ^ ord(b)) for a, b in zip(binKeys[i], binKeys[i + 1])))
        xorDec = [int(i, 2) for i in xorBin]
        return xorBin, xorDec

    def skxor(decKeys, binKeys):
        xorBin =[]
        for i in range(len(binKeys)):
            xorBin.append(''.join(str(ord(a) ^ ord(b)) for a, b in zip(binKeys[i], decKeys[i])))
        return xorBin  

    def mostCommon(data):
        tracker = {}
        for i in data:
            if i in tracker:
                tracker[i] += 1
            else:
                tracker[i] = 1
        appearances = sorted(tracker.items(), key = lambda x : x[1])[::-1]
        values = [i[0] for i in appearances]
        nums = [i[1] for i in appearances]
        return values, nums

    def binDiff(data, font2, font):
        result = []
        for i in range(len(data) - 1):
            formattedNums = []
            for j in range(len(data[i])):
                if int(data[i][j], 2) ^ int(data[i + 1][j], 2):
                    formattedNums.extend([font, data[i][j]])
                else:
                    formattedNums.extend([font2, data[i][j]])
            result.append(formattedNums)
        result.append([font2, data[-1]])
        return result

    def bitNot(data, font2, font):
        nots = []
        for i in range(len(data) - 1):
            formattedNums = []
            string = ""
            for j in range(len(data[i])):
                if data[i][j] == '1':
                    if int(data[i][j], 2) ^ int(data[i + 1][j], 2):
                        formattedNums.extend([font, '0'])
                    else:
                        formattedNums.extend([font2, '0'])
                else:
                    if int(data[i][j], 2) ^ int(data[i + 1][j], 2):
                        formattedNums.extend([font, '1'])
                    else:
                        formattedNums.extend([font2, '1'])
            nots.append(formattedNums)
        nots.append([font2, data[-1]])
        return nots   

    ################################ READ FORMATTED INPUT FILE ##########################
    filename = file
    if os.name == 'nt':
        filename = filename.replace("\"", "").replace("'", "")
    xl = pd.read_excel(filename, 'Seed_Keys_Samples', encoding='utf-8')
    name_in = filename

    ############################### CONVERT INPUT INTO COLUMNS ##########################

    column = list(xl)
    keys = xl[column[1]].dropna()[1:]
    seeds = xl[column[0]].dropna()[1:]

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


    ################################ SETTING UP WORKBOOK ##########################

    calculations = workbook.add_worksheet('Basic Calculations')
    # calculations.set_column(0, 5, 20)
    # calculations.set_column(7, 8, 20)
    # calculations.set_column(10, 10, 20)

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
    binaries = binDiff(binKeys, rFont, font)
    differences = differences(decSeeds, decKeys)
    secondDifferences = sDifferences(differences)
    xorBin, xorDec = xor(binKeys)
    diffs, diffInstances = mostCommon(differences)
    xors, xorInstances = mostCommon(xorDec)
    nots = bitNot(binKeys, rFont, font)
    skxors = skxor(binSeeds, binKeys)
    skxorsdec = [int(i, 2) for i in skxors]

    # write in the column titles for calculations


    # write in the columns for calculations
    def colWriter(sheet, column, name, lst, rich = False):
        maxlen = len(name)
        sheet.write(0, column, name, font)
        for i in range(len(lst)):
            if not rich:
                if len(str(lst[i])) > maxlen:
                    maxlen = len(str(lst[i]))
                sheet.write(i + 1, column, lst[i] , font)
            else:
                if len(str(lst[i])) > maxlen:
                    maxlen = len(str(lst[i][1]))
                sheet.write_rich_string(i + 1, column, *lst[i])    
        sheet.set_column(column, column, maxlen * 1.3)       



    # To add another column, add a tuple to the list in this form: (column index, column name, column list)

    cols = [(0, 'HEX_SEEDS', hexSeeds),
            (1, 'HEX_KEYS',hexKeys),
            (2, 'DEC_SEEDS', decSeeds),
            (3, 'DEC_KEYS', decKeys),
            (4, 'BIN_SEEDS', binSeeds),
            (7, '1st_DIFFERENCES', differences),
            (8, '2nd_DIFFERENCES', secondDifferences),
            (10, 'XOR_BIN', xorBin),
            (11, 'XOR_DEC',xorDec),
            (13, 'APPEARANCES (DIFFERENCES)', diffs),
            (14, "",diffInstances),
            (16, 'APPEARANCES (XOR)', xors),
            (17, "", xorInstances),
            (20 ,'SEED/KEY XOR (BIN)', skxors), 
            (21 ,'SEED/KEY XOR (DEC)', skxorsdec)]

    coloredCols = [(5, 'BIN_KEYS', binaries),
                    (19, 'BIT_NOT', nots)]        

    for i in cols:
        colWriter(calculations, i[0], i[1], i[2])

    for i in coloredCols:
        colWriter(calculations, i[0], i[1], i[2], True)

    calculations.freeze_panes(1, 0)

    ######################### SHIFTS, ROTATES, AND MASKS ##########################################

    rshifts = RshiftAll(binKeys)
    lshifts = LshiftAll(binKeys)
    rotates = rotateAll(binKeys)
    masks = createMasks(binKeys)

    length = len(binKeys[0])

    shifts.set_column(0, length, 9)
    shifts.set_column(length, length * 2, 11)
    shifts.set_column(length * 2, length * 3 - 1, 11)
    row = 0

    cols = []

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
    for i in range(length // 4):
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
    for i in range(length // 4):
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


    seedGraph.add_series({'values' : '=Basic Calculations!$D$2:$D$30',
                          'categories': '=Basic Calculations!$C$2:$C$30'})

    diffGraph.add_series({'values' : '=Basic Calculations!$H$2:$H$30',
                          'categories': '=Basic Calculations!$C$2:$C$30'})

    sdiffGraph.add_series({'values' : '=Basic Calculations!$I$2:$I$30',
                           'categories': '=Basic Calculations!$C$2:$C$30'})

    xorGraph.add_series({'values' : '=Basic Calculations!$L$2:$L$30' ,
                         'categories': '=Basic Calculations!$C$2:$C$30'})

    graphs.insert_chart(1, 1, seedGraph)
    graphs.insert_chart(1, 9, diffGraph)
    graphs.insert_chart(17, 1, sdiffGraph)
    graphs.insert_chart(17, 9, xorGraph)

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