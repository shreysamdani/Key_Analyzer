
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
