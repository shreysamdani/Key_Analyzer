import xlsxwriter

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

def binDiff(data, font, font2):
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

def bitNot(data, font, font2):
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